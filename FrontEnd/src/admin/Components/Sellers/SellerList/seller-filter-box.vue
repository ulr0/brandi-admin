<template>
  <div>
    <a-input-group>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">조회기간</a-col>
        <a-col :span="7">
          <a-range-picker @change="changeDatePicker" :placeholder="['시작일', '종료일']" v-model="filter.rangeDate" />
        </a-col>
      </a-row>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">셀러한글명</a-col>
        <a-col :span="7"><a-input-search placeholder="검색어를 입력해주세요." v-model="filter.korean_name"/></a-col>
        <a-col :span="8">
          <a-input-group compact>
            <a-select v-model="filter.keywordType">
              <a-select-option value="">Select... &nbsp;&nbsp;&nbsp;</a-select-option>
              <a-select-option v-for="item in items" :key="item.value" :value="item.value">{{ item.label }}</a-select-option>
            </a-select>
            <a-input-search placeholder="검색어를 입력해주세요." v-model="filter.keywordValue" style="width: 70%"/>
          </a-input-group>
        </a-col>
      </a-row>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">셀러속성</a-col>
        <a-col :span="22">
          <multi-select-buttons :multiple-select="false" :items="sellerAttribute" v-model="filter.property_id"/>
        </a-col>
      </a-row>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">셀러상태</a-col>
        <a-col :span="22">
          <multi-select-buttons :multiple-select="false" :items="sellerStatus" v-model="filter.status_id"/>
        </a-col>
      </a-row>
    </a-input-group>
    <div class="search-buttons">
      <a-button type="primary" size="large" @click="search">검색</a-button>
      <a-button type="normal" size="large" @click="resetFilter">초기화</a-button>
    </div>
  </div>
</template>

<script>
import MultiSelectButtons from '@/admin/Components/Common/multi-select-buttons'

export default {
  name: 'seller-filter-box',
  props: {
    dataStore: {
      default() {
        return {}
      }
    }
  },
  components: { MultiSelectButtons },
  data() {
    return {
      filter: {
        property_id: [],
        status_id: [],
        korean_name: '',
        keywordType: '',
        keywordValue: '',
        rangeDate: null
      },
      items: [
        { label: '셀러번호', value: 'seller_id' },
        { label: '셀러아이디', value: 'seller_nickname' },
        { label: '셀러영문명', value: 'english_name' },
        { label: '담당자이름', value: 'clerk_name' },
        { label: '담당자연락처', value: 'clerk_phone_number' },
        { label: '담당자이메일', value: 'clerk_email' }
      ]
    }
  },
  computed: {
    constants() {
      return this.$store.state.const
    },
    sellerAttribute() {
      return this.dataStore.sellerAttribute.map(d => { return { value: d.id, label: d.name } })
    },
    sellerStatus() {
      return this.dataStore.sellerStatus.map(d => { return { value: d.id, label: d.name } })
    },
    sellerType() {
      return this.dataStore.sellerType.map(d => { return { value: d.id, label: d.name } })
    }
  },
  created() {
    // 리셋 기능을 위해 clone 데이터 생성
    this.backupFilter = JSON.parse(JSON.stringify(this.filter))
  },
  mounted() {
  },
  methods: {
    search() {
      const filter = this.getFilter()
      this.$emit('search', filter)
    },
    changeDatePicker(v) {
    },
    getFilter() {
      const filter = JSON.parse(JSON.stringify(this.filter))
      if (filter.keywordType && filter.keywordValue) {
        filter[filter.keywordType] = filter.keywordValue
      }
      if (this.filter.rangeDate && this.filter.rangeDate.length === 2) {
        filter.start_date = this.filter.rangeDate[0].format('YYYY-MM-DD')
        filter.end_date = this.filter.rangeDate[1].format('YYYY-MM-DD')
      }
      if (filter.status_id.length > 0) {
        filter.status_id = filter.status_id[0]
      }
      if (filter.property_id.length > 0) {
        filter.property_id = filter.property_id[0]
      }
      delete filter.keywordType
      delete filter.keywordValue
      delete filter.rangeDate
      return filter
    },
    resetFilter() {
      this.filter = JSON.parse(JSON.stringify(this.backupFilter))
      this.search()
    }
  }
}
</script>

<style scoped>
.search-buttons {
  text-align: center;
  margin: 10px 0;
}
.filter-row {
  height: 32px;
  margin: 5px 0;
}
.filter-label {
  font-weight: bold;
  text-indent: 5px;
}
</style>
