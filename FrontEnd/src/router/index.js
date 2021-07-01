import Vue from 'vue'
import Router from 'vue-router'

import AdminLogin from '@/admin/Components/Login/Login'
import AdminSignUp from '@/admin/Components/SignUp/SignUp'

import Admin from '@/admin/Components/Admin'
import AdminSellerDashBoard from '@/admin/Components/SellerDashBoard/SellerDashBoard'

import AdminSellers from '@/admin/Components/Sellers/Sellers'
import AdminSellerList from '@/admin/Components/Sellers/SellerList/SellerList'
import AdminRegisterSeller from '@/admin/Components/Sellers/RegisterSeller/RegisterSeller'

import AdminProducts from '@/admin/Components/Products/Products'
import AdminProductList from '@/admin/Components/Products/ProductList/ProductList'
import AdminRegisterProduct from '@/admin/Components/Products/RegisterProduct/RegisterProduct'

import AdminOrders from '@/admin/Components/Orders/Orders'
import AdminOrderList from '@/admin/Components/Orders/OrderList/OrderList'
import AdminDetailOrder from '@/admin/Components/Orders/DetailOrder/DetailOrder'

// start
// import Cart from '@/service/Cart/Cart'

Vue.use(Router)
export default new Router({
  mode: 'history',
  routes: [
    // 로그인
    {
      path: '/admin/login',
      name: 'Login',
      component: AdminLogin
    },
    {
      path: '/admin/signup',
      name: 'SignUp',
      component: AdminSignUp
    },
    {
      path: '/admin',
      name: 'Admin',
      component: Admin,

      children: [
        // 셀러 대쉬보드
        {
          path: 'sellerdashboard',
          name: 'SellerDashBoard',
          component: AdminSellerDashBoard
        },

        // 회원관리
        {
          path: 'sellers',
          name: 'Sellers',
          component: AdminSellers,

          children: [
            // 회원관리 > 셀러계정관리
            {
              path: '',
              name: 'SellerList',
              component: AdminSellerList
            },
            // 회원관리 > 회원등록
            {
              path: 'registerseller',
              name: 'RegisterSeller',
              component: AdminRegisterSeller
            },
            // 회원관리 > 회원수정
            {
              path: ':sellerNo',
              name: 'ModifySeller',
              component: AdminRegisterSeller,
              props: true
            }
          ]
        },

        // 상품관리
        {
          path: 'products',
          name: 'Products',
          component: AdminProducts,
          children: [
            // 상품관리 > 상품관리
            {
              path: '',
              name: 'ProductList',
              component: AdminProductList
            },
            // 상품관리 > 상품등록
            {
              path: 'registerproduct',
              name: 'RegisterProduct',
              component: AdminRegisterProduct
            },
            // 상품관리 > 상품수정
            {
              path: ':productNo',
              name: 'RegisterProduct',
              component: AdminRegisterProduct
            }
          ]
        },
        // 주문관리
        {
          path: 'orders',
          name: 'Orders',
          component: AdminOrders,
          children: [
            //  주문관리 > 상품준비 관리
            {
              path: 'readyproduct',
              name: 'Readyproduct',
              props: (route) => ({ status_id: 1 }),
              component: AdminOrderList
            },
            // 주문관리 > 배송중 관리
            {
              path: 'deliverproduct',
              name: 'DeliverProduct',
              props: (route) => ({ status_id: 2 }),
              component: AdminOrderList
            },
            // 주문관리 > 배송완료 관리
            {
              path: 'arriveproduct',
              name: 'ArriveProduct',
              props: (route) => ({ status_id: 3 }),
              component: AdminOrderList
            },
            // 주문관리 > 구매확정 관리
            {
              path: 'confirmProduct',
              name: 'ConfirmProduct',
              props: (route) => ({ status_id: 4 }),
              component: AdminOrderList
            },
            // 주문관리 > 주문 상세페이지
            {
              path: ':detailNo',
              name: 'Detail',
              component: AdminDetailOrder,
              props: true
            }
          ]
        }
      ]
    }
    // {
    //   path: '/main',
    //   component: Main
    // },
    // {
    //   path: '/detail/:id',
    //   component: Detail
    // },
    // {
    //   path: '/login',
    //   component: Login
    // },
    // {
    //   path: '/signup',
    //   component: SignUp
    // },
    // {
    //   path: '/order',
    //   component: Order
    // },
    // {
    //   path: '/event',
    //   component: Event,
    //   name: 'event'
    // },
    // {
    //   path: '/event/:no',
    //   component: EventDetail,
    //   name: 'eventDetail'
    // },
    // {
    //   path: '/mypage',
    //   redirect: '/mypage/orderList',
    //   component: Mypage,
    //   name: Mypage,
    //   children: [
    //     {
    //       path: '',
    //       redirect: '/mypage/orderList',
    //       component: OrderList,
    //       name: 'orderList'
    //     },
    //     {
    //       path: 'orderList',
    //       component: OrderList,
    //       name: 'orderList'
    //     },
    //     {
    //       path: 'point',
    //       component: Point,
    //       name: 'point'
    //     },
    //     {
    //       path: 'coupon',
    //       component: Coupon,
    //       name: 'coupon'
    //     },
    //     {
    //       path: 'qna',
    //       component: Mypage,
    //       name: 'qna'
    //     },
    //     {
    //       path: 'faq',
    //       component: Mypage,
    //       name: 'faq'
    //     }
    //   ]
    // },
    // {
    //   path: '/order/detail',
    //   component: OrderDetail
    // },
    // {
    //   // 초기 url을 main으로 적용
    //   path: '/',
    //   redirect: '/main'
    // },
    // {
    //   path: '*',
    //   redirect: '/error/404'
    // },
    // {
    //   path: '/error/400',
    //   component: NetworkError
    // },
    // {
    //   path: '/error/404',
    //   component: NotFound
    // },
    // 회원가입
    // 어드민 내부
  ]
})
