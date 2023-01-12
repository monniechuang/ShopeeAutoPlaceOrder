# -*- coding: UTF-8 -*-


#element Xpath in Shopee
elements = {
    'popup_banner_button':'//div[@data-cy="shopee_popup_close_button"]',
    'login_link':'//a[@data-cy="login_button_home_page"]',
    'username_input':'//input[@name="loginKey"]',
    'password_input':'//input[@name="password"]',
    'login_button':'//button[@data-cy="authentication-pc/login_button_login_page"]',
    'alert_message':'//div[@class="_-packages-user-common-ui-alert-pc-src-components-BaseAlert-style__primaryText"]',
    'account':'//div[@data-cy="username_home_page"]',
    'search_input':'//input[@data-cy="global_input_search_bar_homepage"]',
    'search_button':'//button[@data-cy="global_input_search_icon_homepage"]',
    'search_result_item':'//div[@data-cy="item_card_search_result"]',
    'product_options':'//button[@data-cy="select_payment_icon_checkout_page"]',
    'buy_directly_button':'//button[@data-cy="buy_now_button_product_detail_page"]',
    'go_to_checkout_button':'//button[@data-cy="checkout_button_cart_page"]',
    'bank_transfer_button':'//button[@data-cy="select_payment_icon_checkout_page" and text()="銀行轉帳"]',                           
    'seller_checkoutpage':'//a[@data-cy="page_opc_productdetails_shopname"]',
    'product_name_checkoutpage':'//span[@data-cy="page_opc_product_item_name"]',
    'order_amount_checkoutpage':'//div[@class="_-packages-checkout-page-pc-src-components-OrderSummary-SummaryRow__row _-packages-checkout-page-pc-src-components-OrderSummary-SummaryRow__rowLarge _-packages-checkout-page-pc-src-components-OrderSummary-SummaryRow__rowContent _-packages-checkout-page-pc-src-components-OrderSummary-style__row22"]',
    'place_order_button':'//button[@data-cy="place_order_button_checkout_page"]',
    'bank_transfer_OK_button':'//button[@class="pcmall-paymentfe_src-SafePage-components-Button__button pcmall-paymentfe_src-SafePage-components-Button__primaryButton"]',
    'unexpected_error_OK_button':'//span[@class="payment-popup-button payment-popup-button--main"]',
    'order_status':'//div[@data-cy="order_list_page_order_card_header_status"]',
    'seller_orderlistpage':'//div[@data-cy="order_list_header_seller_name"]',
    'product_name_orderlistpage':'//span[@data-cy="order_list_page_order_card_item_info_name"]',
    'order_amount_orderlistpage':'//div[@data-cy="order_list_order_content_total_price"]'
    }

