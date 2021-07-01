from view.image_view             import ImageView
from view.product_prepare_view   import ProductPrepareView
from view.product_view           import ProductView
from view.product_category_view  import ProductCategoryView
from view.account_view           import SellerAccountView, MasterAccountView, LoginView
from view.master_view            import MasterManageSellerView
from view.search_view            import SearchSellerView
from view.order_detail_info_view import OrderDetailInfoView


def create_endpoints(app):
    app.add_url_rule("/order/product-prepare", view_func=ProductPrepareView.as_view("product_prepare"))
    app.add_url_rule("/join/sellers", view_func=SellerAccountView.as_view("seller_account_view"))
    app.add_url_rule("/join/masters", view_func=MasterAccountView.as_view("master_account_view"))
    app.add_url_rule("/login", view_func=LoginView.as_view("login_view"))
    app.add_url_rule("/order/product-prepare/download", view_func=ProductPrepareView.as_view("product_prepare_excel_download"))
    app.add_url_rule("/order/order-detail-info", view_func=OrderDetailInfoView.as_view("order_detail_info"))
    app.add_url_rule("/manage/sellers", view_func=MasterManageSellerView.as_view("master_manage_seller_view"))
    app.add_url_rule("/manage/sellers/downloads", view_func=MasterManageSellerView.as_view("master_manage_seller_download_view"))
    app.add_url_rule("/search/sellers", view_func=SearchSellerView.as_view("search_seller"))
    app.add_url_rule("/products", view_func=ProductView.as_view("product"))
    app.add_url_rule("/products/categories/<int:seller_category_id>", view_func=ProductCategoryView.as_view("product_category"))
    app.add_url_rule("/products/categories/<int:seller_category_id>/<int:product_category_id>", view_func=ProductCategoryView.as_view("product_subcategory"))
    app.add_url_rule("/images", view_func=ImageView.as_view("image"))
