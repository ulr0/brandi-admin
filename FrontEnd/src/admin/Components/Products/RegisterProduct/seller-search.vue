<template>
  <a-select
    show-search
    :value="value"
    placeholder="셀러검색"
    style="width: 200px"
    :default-active-first-option="false"
    :show-arrow="false"
    :filter-option="false"
    :not-found-content="null"
    @search="handleSearch"
    @change="handleChange"
  >
    <a-select-option v-for="d in data" :key="d.value">
      {{ d.text }}
    </a-select-option>
  </a-select>
</template>

<script>
import AdminApiMixin from '@/admin/mixins/admin-api'
import CommonMixin from '@/admin/mixins/common-mixin'
export default {
  mixins: [AdminApiMixin, CommonMixin],
  data() {
    return {
      data: [],
      value: undefined
    }
  },
  methods: {
    async handleSearch(value) {
      console.log('handleSearch', value)
      const res = await this.searchSeller(value)
      console.log(res.data.result)
      this.data = res.data.data.sellers.map(d => {
        return { value: d.Id, text: d.korean_name, seller_subcategory_id: d.seller_subcategory_id }
      })
      // fetch(value, data => (this.data = data))
    },
    async handleChange(value) {
      console.log('handleChange', value)
      this.value = value
      // const res = await this.searchSeller(value)
      const findItem = this.data.find(item => { return item.value === value })
      // console.log(findItem)
      // fetch(value, data => (this.data = data))
      this.$emit('input', findItem)
    },
    searchSeller(name) {
      return this.get(this.searchUrl, {
        params: { search_word: name, limit: 10 }
      })
    }
  },
  computed: {
    prefixUrl() {
      return this.constants.apiDomain
    },
    searchUrl() {
      return this.prefixUrl + '/search/sellers'
    }
  }

}
</script>

<style lang="scss" scoped>

</style>
