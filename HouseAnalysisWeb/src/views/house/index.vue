<template>
  <div class="wrapper">
    <search @gethouse="gethouse" />

    <el-row style="margin-left: 20px">
      <el-col :span="18">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="1">全部房源</el-menu-item>
          <el-menu-item index="2">默认</el-menu-item>
          <el-menu-item index="3">总价</el-menu-item>
          <el-menu-item index="4">单价</el-menu-item>
          <el-menu-item index="5">面积</el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
    <div
      v-loading="loading"
      class="loadingwrapper"
      lock="true"
      element-loading-background="rgb(255, 255, 255)"
      element-loading-text="正在加载中"
    />
    <el-row style="margin-left: 10px">
      <el-col :span="18">
        <div class="title">共找到 <span>{{ housePaginationData.totalNumber }}</span> 套成都二手房</div>
        <ul class="houselist">
          <li v-for="house in houselist" :key="house.id" class="houseitem">
            <router-link target="_blank" :to="{path:'/show/houseinfo',query: {id: house.id}}">
              <div class="leftimg" :style="{background: 'url('+ house.image_urls.match(/'(.+?)'/g)[0].replace(/\'/g,'') +') no-repeat',backgroundSize:'cover'}" />
            </router-link>
            <div class="rightinfo">
              <router-link target="_blank" :to="{path:'/show/houseinfo',query: {id: house.id}}">
                <p>{{ house.title }}</p>
              </router-link>
              <div class="price">
                <span>
                  {{ house.price }} <i>万</i>
                </span>
                <span>
                  单价{{ house.unit_price }}元/平米
                </span>
              </div>
              <div><i class="el-icon-location" />{{ house.community_name }} | {{ house.region | parseArray }}</div>
              <div><i class="el-icon-arrow-right" />{{ house.type }} | {{ house.construction_area }} | {{ house.orientation }} | {{ house.decoration }}</div>
              <div><i class="el-icon-time" />{{ house.elevator }} | {{ house.floor }} | {{ house.purposes }}</div>
            </div>
          </li>
        </ul>
      </el-col>
    </el-row>
    <el-row style="height: 100px;">
      <div class="commpage">
        <pagination :pagination-data="housePaginationData" />
      </div>
    </el-row>
  </div>
</template>

<script>
import { getAll, getOrderHouse } from '@/api/charts.js'
import Search from '@/components/Search'
import Pagination from '@/components/Pagination'
import { Notification } from 'element-ui';

export default {
  components: {
    Search,
    Pagination
  },
  filters: {
    parseArray: function(value) {
      if (!value) return ''
      return value.replace(/\[|\]|'/g, '').split(',').join('-')
    },
    getimg: function(value) {
      re_data = value.match(/'(.+?)'/g)
      first_img = re_data[0].replace(/\'/g, '')
      return first_img
    }
  },
  data() {
    return {
      loading: true,
      pagenums: 0,
      houselist: [],
      activeIndex: '1',
      value: '',
      tag: '',
      housePaginationData: {
        pageSize: 30,
        currentPage: 1,
        totalNumber: 0,
        handleCurrentChange: psize => {
          this.housePaginationData.currentPage = psize
          this.handleClick(this.value, psize)
        }
      }
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      this.loading = true
      this.housePaginationData.currentPage = 1
      const tags = ['', 'price', 'unit_price', 'construction_area']
      let params = {}
      if(key != 1) {
        this.tag = tags[key-2]
        params = {
          ordering: tags[key-2],
          search: this.value
        }
      } else {
        this.tag = ''
      }
      getOrderHouse(params).then((res, err) => {
        this.housePaginationData.totalNumber = res.count
        this.houselist = res.results
        this.loading = false
      })
    },
    gethouse(data) {
      this.loading = true
      const totalData = data.res
      this.value = data.value
      this.housePaginationData.totalNumber = totalData.count
      this.houselist = totalData.results
      this.loading = false
    },
    handleClick(inputVal, page) {
      try {
        let params = {}
        params = {
          ordering: this.tag,
          search: inputVal,
          page: page
        }
        getOrderHouse(params).then((res, err) => {
          this.houselist = res.results
        })
      } catch (err) {
        console.log('请求失败', err)
      }
    }
  }
}
</script>

<style lang="scss">
.wrapper {
  width: 100%;
  height: 100%;
  margin-left: 50px;

  .loadingwrapper {
    width: 100%;
    height: 600px;
    position: absolute;
  }
}
  .title {
    height: 55px;
    line-height:55px;
    word-spacing:0;
    font-size:22px;
    font-weight:600;

    span {
      color: #00AE66;
    }
  }

  .houselist {
    padding:0;
    width: 910px;
  }

  .houseitem {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    display: block;
    height: 194px;
    border-bottom:1px solid #f1f1f1;
    margin: 10px 0;

    .leftimg {
      float: left;
      width: 232px;
      height: 100%;
      cursor: pointer;
    }
    .rightinfo {
      float: right;
      width: 640px;
      height: 100%;

      p {
        height: 15px;
        line-height:15px;
        word-spacing:0;
        font-size:22px;
        font-weight:600;
        margin-left:10px;
      }
      p:hover {
        color: #00AE66;
      }

      div {
        height:25px;
        line-height: 25px;
        font-size: 15px;
        color: #616669;
        white-space: nowrap;
        margin: 10px;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;

        i {
          margin-right:7px;
        }
      }

      .price {
        float: right;
        margin-right:20px;

        span {
          display: block;
        }

        span:nth-child(1) {
          color: #DB4C3F;
          height: 30px;
          line-height:30px;
          font-size:26px;
          font-weight:700;
          margin-right:13px;

          i {
            font-size:14px;
          }
        }

        span:nth-child(2) {
          height: 16px;
          line-height:16px;
          font-size:12px;
        }
      }
    }
  }
.commpage {
  width: 100%;
  height: 100%;
  position: absolute;
  top:10px;
  bottom:18px;
  left:22%;
}
</style>
