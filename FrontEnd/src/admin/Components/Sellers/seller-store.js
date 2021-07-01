import store from '@/store/index'
import AdminApiMixin from '@/admin/mixins/admin-api'
import CommonMixin from '@/admin/mixins/common-mixin'
import Message from '@/admin/utils/message'
// import mockup from '@/admin/mockup/sellerList.json'

export default {
  store: store,
  mixins: [AdminApiMixin, CommonMixin],
  data() {
    return {
      sellerNo: 0, // 셀러 번호 (상세에서 사용함)
      list: [],
      page: 1,
      total: 0,
      pageLen: 10,
      loading: false,
      filter: {},
      detailData: {},
      backupDetailData: {},
      sellerAttribute: [], // 셀러 속성 (쇼핑몰...)
      sellerStatus: [], // 셀러 상태 (입점...)
      sellerType: [] // 셀러 구분 (일반, 헬피)
    }
  },
  created() {
    if (this.isMaster()) {
      this.getMeta()
    }
  },
  computed: {
    prefixUrl() {
      return this.constants.apiDomain
    },
    maxPage() {
      return Math.ceil(this.total / this.pageLen)
    },
    constants() {
      return this.$store.state.const
    },
    // 셀러 리스트 / 수정
    listUrl() {
      return this.prefixUrl + '/manage/sellers'
    },
    // 셀러 리스트 / 수정
    getUrl() {
      return this.prefixUrl + '/sellers'
    },
    // 셀러 상태 변경
    patchUrl() {
      return this.prefixUrl + '/manage/sellers'
    },
    // 셀러 리스트 / 수정
    putUrl() {
      return this.prefixUrl + '/edit'
    },
    metaUrl() {
      return this.prefixUrl + '/account/init'
    },
    // 셀러 리스트 / 수정
    statusUrl() {
      return this.prefixUrl + '/manage/sellers'
    },
    offset() {
      return (this.page - 1) * this.pageLen
    }
  },
  methods: {
    loadData() {
      this.get(this.prefixUrl + '/edit')
        .then(response => {
          console.log('response', response)
        })
        .then(() => {
          // this.$router.push('/admin/sellerdashboard')
        })
        .catch(e => {
          Message.error(e.response.data.message)
        })
    },
    load() {
      this.loading = true
      const params = JSON.parse(JSON.stringify(this.filter))
      params.limit = this.pageLen
      params.offset = (this.page - 1) * this.pageLen

      // this.get(this.constants.apiDomain + '/seller/edit')
      this.get(this.listUrl, {
        params: params
      })
        .then((res) => {
          if (res.data) {
            const sellerList = res.data.data
            const totalCount = res.data.count
            sellerList.forEach((d) => {
              d.checked = false
            })
            this.total = totalCount
            this.list = sellerList
          } else {
            Message.error('통신 실패')
          }
        }).catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.')
          } else {
            Message.error(e.response.data.message)
          }
        }).then((res) => {
          this.loading = false
        })
    },
    changeStatus(sellerId, toStatusTypeId) {
      this.loading = true
      const payload = {
        seller_id: sellerId,
        master_action_id: toStatusTypeId
      }
      this.patch(this.statusUrl, payload)
        .then((res) => {
          Message.success('셀러 상태 변경 성공')
          this.load()
        })
        .catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error({
              content: '요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.'
            })
          } else {
            Message.error({
              content: e.response.data.message
            })
          }
        }).then((res) => {
          this.loading = false
        })
    },
    getDetail(sellerId) {
      this.loading = true
      const url = this.getUrl + '/' + sellerId
      // if (this.isMaster()) url += sellerId
      this.get(url)
        .then((res) => {
          if (res.data) {
            this.detailData = res.data.result
            if (!this.detailData.managers || this.detailData.managers.length === 0) {
              this.detailData.managers = [{}]
            }
            this.backupDetailData = JSON.parse(JSON.stringify(this.detailData))
          } else {
            Message.error('통신 실패')
          }
        }).catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.')
          } else {
            Message.error(e.response.data.message)
          }
        }).then((res) => {
          this.loading = false
        })
    },
    putDetail(sellerId, sellerData) {
      // managers
      debugger
      const payload = JSON.parse(JSON.stringify(this.detailData))
      delete payload.managers
      this.loading = true
      this.patch(this.patchUrl, payload)
        .then((res) => {
          Message.success('셀러 수정 성공')
          this.backupDetailData = JSON.parse(JSON.stringify(this.detailData))
        }).catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.')
          } else {
            Message.error(e.response.data.message)
          }
        }).then((res) => {
          this.loading = false
        })
    },
    getMeta() {
      this.get(this.metaUrl)
        .then((res) => {
          if (res.data) {
            this.sellerAttribute = res.data.result.data.sellerAttribute
            this.sellerStatus = res.data.result.data.sellerStatus
            this.sellerType = res.data.result.data.sellerType
          } else {
            Message.error('통신 실패')
          }
        }).catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.')
          } else {
            Message.error(e.response.data.message)
          }
        }).then((res) => {
          // this.loading = false
        })
    },
    changePage(page) {
      this.page = page
      this.load()
    },
    setFilter(filter) {
      this.filter = filter
    }
  },
  watch: {
    pageLen(v) {
      this.changePage(1)
    }
  }
}
