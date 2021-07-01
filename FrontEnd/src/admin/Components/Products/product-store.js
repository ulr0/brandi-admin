import AdminApiMixin from '@/admin/mixins/admin-api'
import CommonMixin from '@/admin/mixins/common-mixin'
import errors from '@/admin/errors/errors'
// import mockup from '@/admin/mockup/productList.json'
import Message from '@/admin/utils/message'
import moment from 'moment'
// import router from '@/router'
const ExpireTokenException = errors.ExpireTokenException
const TimeoutException = errors.TimeoutException

export default {
  mixins: [AdminApiMixin, CommonMixin],
  data() {
    return {
      list: [],
      page: 1,
      total: 0,
      pageLen: 10,
      loading: false,
      isNew: true, // 신규 등록 여부
      filter: {},
      colors: [],
      sizes: [],
      productCategory: [],
      productSubCategory: [],
      backupDetailData: {},
      detailData: {
        basic_info: {
          seller_id: ''
        },
        manufacturer: '', // 제조사
        manufactured_date: '', // 제조일
        origin_id: 0, // 원산지 아이디
        is_sold: 0, // 판매여부
        is_displayed: 0, // 진열여부
        selling_info: {},
        // option_info: [],
        images: ['', '', '', '', ''],
        category_id: null, // 1차 카테고리
        product_subcategory_id: null, // 2차 카테고리
        seller_property_id: 1,
        name: '', // 상품명
        brand_name_korean: '',
        gosiType: 1,
        detail_page_html: '', // 상품 상세 정보
        price: 0, // 판매가
        minimum_sell_quantity: 1, // 최소 수량
        maximum_sell_quantity: 20, // 최대 수량
        discount_rate: 0, // 할인율
        discountPrice: 0, // 할인가
        discount_start_time: '', // 할인시작일
        discount_end_time: '', // 할인종료일
        option_info: [] // 옵션 상품
      }
    }
  },
  props: {
    router: {
      default() {
        return null
      }
    }
  },
  created() {
    // this.load();
  },
  computed: {
    prefixUrl() {
      return this.constants.apiDomain
    },
    maxPage() {
      return Math.ceil(this.total / this.pageLen)
    },
    // 셀러 리스트 / 수정
    listUrl() {
      return this.prefixUrl + '/products'
    },
    batchUrl() {
      return this.prefixUrl + '/products'
    },
    // 상품 리스트 / 수정
    getUrl() {
      return this.prefixUrl + '/products'
    },
    // 셀러 상세
    getSellerUrl() {
      return this.prefixUrl + '/search/sellers'
    },
    // 상품 컬러 리스트
    getColorUrl() {
      return this.prefixUrl + '/products/color'
    },
    // 상품 사이즈 리스트
    getSizeUrl() {
      return this.prefixUrl + '/products/size'
    },
    // 셀러 리스트 / 수정
    postUrl() {
      return this.prefixUrl + '/products'
    },
    // 셀러 리스트 / 수정
    putUrl() {
      return this.prefixUrl + '/products'
    },
    // 셀러 리스트 / 수정
    metaUrl() {
      return this.prefixUrl + '/product/management/init'
    },
    // 셀러 1차 카테고리
    sellerInfoUrl() {
      return this.prefixUrl + '/products/categories'
    },
    // 셀러 2차 카테고리
    sellerSubCategoryUrl() {
      return this.prefixUrl + '/products/categories'
    },
    offset() {
      return (this.page - 1) * this.pageLen
    }
  },
  methods: {
    load() {
      this.loading = true
      const params = JSON.parse(JSON.stringify(this.filter))
      params.limit = this.pageLen
      params.offset = this.offset

      return new Promise((resolve, reject) => {
        // 아래는 테스트 코드
        // new Promise((_resolve, _reject)=>{
        //     setTimeout(()=>{
        //         // router.push('/')
        //         _reject(tokenExpireMockup())
        //     }, 300)
        // })
        // new Promise((resolve, reject) => {
        //   setTimeout(() => {
        //     this.$emit('test', { a: 1 })
        //     resolve(listMockup())
        //   }, 300)
        // })
        // 실제 연동은 아래
        this.get(this.listUrl, {
          params: params
        })
          .then((res) => {
            if (res.data && res.data.data.count !== undefined) {
              res.data.data.products.forEach((d) => {
                d.checked = false
              })
              const productList = res.data.data.products
              const totalCount = res.data.data.count
              this.total = totalCount
              this.list = productList
              resolve()
            } else {
              // eslint-disable-next-line prefer-promise-reject-errors
              reject('통신 실패')
            }
          }).catch((e) => {
            // TODO 타임아웃 처리를 공통으로 할 수 있을까?
            if (e.code === 'ECONNABORTED') {
              reject(new TimeoutException('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.'))
            } else if (e.response && e.response.data.message === 'INVALID TOKEN') {
              reject(new ExpireTokenException('로그인이 만료 되었습니다. 다시 로그인 해주세요.'))
            } else {
              // eslint-disable-next-line prefer-promise-reject-errors
              reject('처리 중 오류 발생')
            }
          }).then((res) => {
            this.loading = false
          })
      })
    },
    getDetail(productId, callback) {
      this.get(this.getUrl + '/' + productId)
        .then(res => {
          // this.backupDetailData = JSON.parse(JSON.stringify(res.data.result))
          const response = JSON.parse(JSON.stringify(res.data.result))
          // for (let i = 0; i < 5; i++) {
          //   if (response.productThumbnails[i] && response.productThumbnails[i].imageUrl) {
          //     response.productThumbnailImages[i] = response.productThumbnails[i].imageUrl
          //   } else {
          //     response.productThumbnailImages[i] = ''
          //   }
          // }
          response.images = response.basic_info.images.map(d => { return d.image_url })
          this.detailData = response
          if (callback) {
            callback(this.detailData)
          }
        })
    },
    async getSellerDetail(sellerTypeNo) {
      const res = await this.get(this.sellerInfoUrl + '/' + sellerTypeNo)
      this.productCategory = res.data.data.product_categories
      // /products/sellers/<int:seller_id>
    },
    async getSellerSubCategory(categoryId) {
      const res = await this.get(this.sellerSubCategoryUrl + '/' + this.detailData.category_id + '/' + categoryId)
      this.productSubCategory = res.data.data.product_subcategories
    },
    putProduct(productId) {
      const images = this.detailData.images
      const payload = JSON.parse(JSON.stringify(this.detailData))
      payload.basic_info.date_of_manufacture = moment(payload.basic_info.date_of_manufacture).format('YYYY-MM-DD')
      payload.images = payload.images.filter(d => d).splice(0, 5)
      // deleteProductThumbnails 삭제 (기존에 있고, 현재 없는거)
      // payload.deleteProductThumbnails = this.detailData.productThumbnails.filter(d => {
      //   // console.log(d.imageUrl, payload.productThumbnailImages, payload.productThumbnailImages.includes(d.imageUrl))
      //   if (!payload.productThumbnailImages.includes(d.imageUrl)) return true
      //   return false
      // }).map(d => d.productThumbnailId)
      // productThumbnailImages 신규 등록
      // payload.productThumbnailImages = payload.productThumbnailImages.filter(d => {
      //   // console.log(this.detailData.productThumbnails, d, this.detailData.productThumbnails.includes(d))
      //   const findList = this.detailData.productThumbnails.find(dd => dd.imageUrl === d)
      //   if (!findList) return true
      //   return false
      // })
      // console.log(payload)
      const formData = new FormData()
      formData.append('payload', JSON.stringify(payload))
      images.forEach(file => {
        if (file) {
          formData.append('file', file)
        }
      })

      this.patch(this.putUrl + '/' + productId, formData)
        .then(res => {
          Message.success('상품 수정 성공')
        })
    },
    getMeta() {
      this.get(this.metaUrl)
        .then(res => {
          this.productCategory = res.data.result.product_categories
          this.colors = res.data.result.product_colors
          this.sizes = res.data.result.product_sizes
        })
    },
    getColorList() {
      this.get(this.getColorUrl)
        .then(res => {
          this.colors = res.data.result
        })
    },
    getSizeList() {
      this.get(this.getSizeUrl)
        .then(res => {
          this.sizes = res.data.result
        })
    },
    addProduct() {
      /*
      --form 'seller_id="2"' \
    --form 'is_sold="true"' \
    --form 'is_displayed="true"' \
    --form 'product_subcategory_id="2"' \
    --form 'manufacturer="서진물산"' \
    --form 'manufactured_date="2021-05-21"' \
    --form 'origin_id="1"' \
    --form 'name="testname"' \
    --form 'comment="하늘하늘"' \
    --form 'main_image_file=@"/Users/cold/Downloads/20200122230101_wxuhplzv.jpeg"' \
    --form 'image_files=@"/Users/cold/Downloads/g4830g64697295p8t2n9.jpeg"' \
    --form 'image_files=@"/Users/cold/Downloads/i16288330962.jpeg"' \
    --form 'detail_page_html="<html></html>"' \
    --form 'options="{\"color_id\":\"1\", \"size_id\":\"2\"},{\"color_id\":\"2\", \"size_id\":\"1\"}"' \
    --form 'price="10000"' \
    --form 'discount_rate="10"' \
    --form 'discount_start_time="2021-05-26 15:10"' \
    --form 'discount_end_time="2021-05-27 15:10"' \
    --form 'minimum_sell_quantity="1"' \
    --form 'maximum_sell_quantity="20"'
      */
      const payload = JSON.parse(JSON.stringify(this.detailData))
      payload.basic_info.date_of_manufacture = moment(payload.basic_info.date_of_manufacture).format('YYYY-MM-DD')
      const images = this.detailData.images
      delete payload.images
      const formData = new FormData()
      formData.append('payload', JSON.stringify(payload))
      images.forEach(file => {
        if (file) {
          formData.append('file', file)
        }
      })
      console.log(formData)
      // eslint-disable-next-line no-constant-condition
      if (true) {
        return
      }

      // payload.productThumbnailImages = payload.productThumbnailImages.filter(d => d)
      this.post(this.postUrl, formData)
        .then(response => {
          Message.success('상품이 일괄 수정 되었습니다.')
        })
        .then(() => {
          Message.success('상품이 일괄 수정 되었습니다.', () => {
          })
        })
        .catch(err => {
          if (err.response) {
            console.log(err.response)
            console.log(err.response.message)
          }
          Message.error('상품 일괄 수정에 실패하였습니다.')
        })

      // const payload = JSON.parse(JSON.stringify(this.detailData))
      // payload.productThumbnailImages = payload.productThumbnailImages.filter(d => d)
      // this.post(this.postUrl, payload)
      //   .then(response => {
      //     Message.success('상품이 일괄 수정 되었습니다.')
      //   })
      //   .then(() => {
      //     Message.success('상품이 일괄 수정 되었습니다.', () => {
      //     })
      //   })
      //   .catch(err => {
      //     if (err.response) {
      //       console.log(err.response)
      //       console.log(err.response.message)
      //     }
      //     Message.error('상품 일괄 수정에 실패하였습니다.')
      //   })
    },
    changePage(page) {
      this.page = page
    },
    setFilter(filter) {
      this.filter = filter
    },
    getCheckedList() {
      return this.list.filter(d => {
        return d.checked
      })
    },
    async batchUpdate(productList, updateValue) {
      // 상품 일괄 수정
      const payload = []
      productList.forEach(product => {
        const updataData = { product_id: product.product_number }
        if (updateValue.selling !== '') {
          updataData.is_sold = updateValue.selling === '1'
        }
        if (updateValue.display !== '') {
          updataData.is_displayed = updateValue.display === '1'
        }
        payload.push(updataData)
      })
      try {
        // const response =
        const res = await this.patch(this.batchUrl, payload)
        // 일괄 처리 실패 있음
        const failCount = res.data.data.fail_list.length
        if (failCount > 0) {
          // 전체 실패
          if (failCount === productList.length) {
            // 일부 실패
            Message.error('상품이 일괄 수정이 모두 실패하였습니다.')
          } else {
            // 일부 실패
            Message.warn(`상품이 일괄 수정 되었고 ${failCount}건의 주문의 갱신이 실패하였습니다.`)
          }
        } else {
          Message.success('상품이 일괄 수정 되었습니다.')
        }
        updateValue.selling = ''
        updateValue.display = ''
        this.load()
      } catch (err) {
        console.log(err)
        Message.error('상품이 일괄 수정에 실패하였습니다. ' + err.response.user_error_message)
      }
    }
  },
  watch: {
    pageLen(v) {
      this.changePage(1)
    }
  }
}

// function listMockup() {
//   return mockup
// }
