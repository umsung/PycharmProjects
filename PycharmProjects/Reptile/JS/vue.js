    //超值换购
    var tradeInProduct = "[";
    //超值换购
    $('.tradeInProduct-list .check-k').each(
        function () {
            if ($(this).prop("checked")) {
                var productCount = $(this).parent().siblings(".num-tradeInProduct").children(".shop-num-tradeInProduct").children(".input-num-tradeInProduct").children("input").val();
                tradeInProduct += "{productId:" + parseInt($(this).attr("data-productId")) + ",productCount:" + parseInt(productCount) + "},";
            }
        }
    );

    tradeInProduct = tradeInProduct.substring(0, tradeInProduct.length - 1) + "]";
    if (tradeInProduct == "]") {
        tradeInProduct = "";
    }



    //---代金券相关 START--------

function showCoupon() {
    $("#vue_content").hide();
    $("#yhqContent").fadeIn(300);
    $(".pagetit").text("使用代金券");
}

function back() {
    if ($("#yhqContent").length > 0) {
        if ($(".pagetit").text() == "确认订单") {
            window.location.href = "javascript:history.back(-1);";
        }
        else {
            $("#vue_content").show();
            $("#yhqContent").fadeOut(200);
            $(".pagetit").text("确认订单");
        }
    }
}
/**
 * 激活代金券
 */
function ActiveMyCoupon() {
    var code = $.trim($("#couponCode").val());
    if (code.length == 0) {
        alert("请输入代金券激活码！");
        return;
    }
    var params = { code: code, productId_QuantityStr: $("#SelectedProductId_QuantityStr").val() };
    $.ajax({
        url: "/order/ActivateCouponInConfirm",
        type: "post",
        data: $.param(params),
        success: function (data) {
            if (data.Result) {
                $("#couponCode").val("");

                if (data.IsCanUse) {
                    LoadMyCouponData(null);
                    alert(data.Msg);
                } else {
                    //alert("代金券激活成功，但该代金券不能在本订单中使用!<br />请在会员中心的“我的代金券”中查看详情");
                    $(".popdiv").show();
                }
            }
            else {
                alert(data.Msg);
            }
        }
    });
}

var orderData = {
    originTotalPrice: 0,
    finalTotalPrice: 0,   
    vipDiscountPrice: 0,
    fullFreePrice: 0,
    fullDiscountPrice: 0,    
    wineWorldCoupon: {
        own: 0,
        pay:0,
    },
    wineCoupon: {
        own: 0,
        pay: 0,
    },
    zmCoupon: {
        own: 0,
        pay: 0,
    },
    productCoupon: {
        count: 0,
        selectedCoupon: "",
        couponDiscountPrice: 0,
    },
    tradeInService: {
        count: 0,
        totalPrice: 0,
        payZMJF: 0
    },
    gainTotalZMJF: 0,
    payTotalZMJF: 0,
    totalCount: 0
}
var price = parseInt($("#totalPrice").data("price"));
var myCouponIds = "";
var myProductCouponTotalPrice = 0;
var myCouponCategoryId_Count_Info = "";
/**
 * 选择代金券
 * @param {any} e
 */
function selectUseCoupon(e) {

    if ($(e).find(".c-check").hasClass("coup-checked")) {
        if (myCouponIds.indexOf($(e).find(".userSelect").val() + "|") != -1) {
            myCouponIds = myCouponIds.replace($(e).find(".userSelect").val() + "|", "");
        }
    }
    else {
        myCouponIds += $(e).find(".userSelect").val() + "|";
    }

    var userSelect = myCouponIds;
    if (myCouponIds.lastIndexOf("|") == myCouponIds.length - 1) {//最后一个字符是|，剪切
        userSelect = myCouponIds.substr(0, myCouponIds.length - 1);
    }
    if (userSelect == "") {
        userSelect = "0";
    }

    myCouponIds = "";
    myProductCouponTotalPrice = 0;

    LoadMyCouponData(userSelect);
    $("html,body").animate({ scrollTop: 0 }, "fast");
}

function GetMyUseCouponCategoryId_UseCount_Str() {
    return myCouponCategoryId_Count_Info;
}
/**
 * 加载我可用的代金券
 */
function LoadMyCouponData(userSelect) {

    if (!userSelect) {
        orderData.productCoupon = {
            count: 0,
            selectedCoupon: "",
            couponDiscountPrice: 0,
        };
    }

    var params = {
        userSelect: userSelect,
        productId_QuantityStr: $("#SelectedProductId_QuantityStr").val(),
    };

    $.ajax({
        type: "POST",
        url: "/Order/RefreshMyCoupon",
        data: $.param(params),
        success: function (data) {
            $("#lstMyProductCoupons").empty();
            if (!data.Result) {
                alert("获取代金券异常，请稍后再试！");
                return;
            }
            if (data.Data.length == 0 || typeof (data.Data) == "undefined") {
                
                $("#couponMoney").text(0);
                $("#couponNum").text(0);

                orderData.productCoupon = {
                    count: 0,
                    selectedCoupon: "",
                    couponDiscountPrice: 0
                };

                myCouponCategoryId_Count_Info = "";
                return;
            }

            ww.load('j.jtemplates', function () {
                var coupons = { Data: data.Data };
                $("#lstMyProductCoupons").setTemplateURL("/Templ/CouponList.htm?rd=" + Math.random(), null, { filter_data: false });
                $("#lstMyProductCoupons").processTemplate(coupons);
            });

            canUseCoupons = data.Data;
            if (typeof (canUseCoupons) != "undefined" && canUseCoupons.length > 0) {
                orderData.zmCoupon.pay = 0;
                orderData.wineCoupon.pay = 0;
                orderData.wineWorldCoupon.pay = 0;
               
                //orderData.fullFreePrice = parseInt($("#temp_FullFreePrice").val());
                //orderData.fullDiscountPrice = parseInt($("#temp_FullDiscountPrice").val());
                //orderData.vipDiscountPrice = parseFloat($("#temp_vipTotalDiscount").val());
                orderData.gainTotalZMJF = parseInt($("#temp_gainZMJF").val());
                //orderData.payTotalZMJF = parseInt($("#temp_payZMJF").val());
                //orderData.originTotalPrice = parseInt($("#temp_originTotalPrice").val());

                CalculateUseCouponsPrice(canUseCoupons);
            } else {
                $("#couponMoney").text(0);
                $("#couponNum").text(0);
            }
        }
    });
}

/**
 * 计算用券后的价格
 * @param {any} coupons
 */
function CalculateUseCouponsPrice(coupons) {
    var couponMoney = 0;
    var couponNum = 0;
    var tempCouponCategoryIds = "";
    var isBuyCode = $("#isBuyCode").val();
    //--代金券类型|1;代金券类型|1;
    var t_vipPrice = 0; // 总折扣
    var t_originPrice = 0; //总原价
    var t_getIntegrationValue = orderData.gainTotalZMJF;
    productList = [];
    $(".cell-productItem").each(function (e) {
        var pid = parseInt($(this).data("pid"));
        var vipprice = parseFloat($(this).data("vipprice"));
        var orgprice = parseFloat($(this).data("orgprice"));
        var unitprice = parseFloat($(this).data("unitprice"));
        var quantity = parseFloat($(this).data("quntity"));
        var spec = $(this).data("spec");
        var isVipAndAgentWine = $(this).data("vipagent") == 'True';
        var discountType = $(this).data("discounttype");
        var getIntegrationValue = parseFloat($(this).data("getintegrationvalue"));     
        
        if (discountType === "Promotion" || isBuyCode) { // 活动优惠 OR 购买码购买
            orgprice = unitprice;
        }
        vipprice = vipprice || orgprice;
        var product = {
            pid: pid,
            orgprice: orgprice,
            vipprice: vipprice,
            getIntegrationValue: getIntegrationValue,
            quantity: quantity,
            isVipAndAgentWine: isVipAndAgentWine,
            spec: spec
        };
        productList.push(product);
        
        if (isVipAndAgentWine) { // 享受独代酒款买一送一
            t_vipPrice += (orgprice - vipprice) * quantity;
            t_originPrice += vipprice * quantity;
        } else {
            t_originPrice += orgprice * quantity;
        }
    });

    var c_discountMoney = 0; // 用券折扣的钱
    var totalPrice = 0;
    var chosedCouponCase = "None";
    for (var i = 0; i < coupons.length; i++) {
        // 判断选券情况
        if (String(coupons[i].State) == "1") {
            //折扣优惠券分类
            if (String(coupons[i].Category) == "2") {
                if (String(coupons[i].IsGeneralCommon) == 'true') {
                    chosedCouponCase = "UniversalDiscountCoupon";
                    break;
                } else {
                    chosedCouponCase = "LimitDiscountCoupon";
                    break;
                }
            }
            //满减优惠券分类
            else if (String(coupons[i].Category) == "3") {
                if (String(coupons[i].IsGeneralCommon) == 'true') {
                    //全场
                    chosedCouponCase = "UniversalFullReduceCoupon";
                    break;
                } else {
                    //指定商品
                    chosedCouponCase = "LimitFullReduceCoupon";
                    break;
                }
            }
            else if (String(coupons[i].Category) == "1") {
                chosedCouponCase = "UsualCoupon";
                break;
            }
        }
    }

    // 使用通固定金额代金券券
    if (chosedCouponCase == "UsualCoupon") { 

        // 计算不再区分全场还是固定金额代金券
        var uCoupons = []; // 固定金额代金券列表
        $.each(coupons, function (index, coupon) {
            if (String(coupon.State) == "1" && String(coupon.Category) == "1") {
                uCoupons.push(coupon);
            }
        });

        t_vipPrice = 0;
        var products = [];
        // 将商品按照数量拆分
        for (var i = 0; i < productList.length; i++) {
            for (var j = 0; j < productList[i].quantity; j++) {
                products.push({
                    pid: productList[i].pid,
                    orgprice: productList[i].orgprice,
                    vipprice: productList[i].vipprice,
                    getIntegrationValue: productList[i].getIntegrationValue,
                    isVipAndAgentWine: productList[i].isVipAndAgentWine
                });
            }
        }

        if (uCoupons.length > 0) {
            for (var i = products.length - 1; i >= 0; i--) {
                for (var j = uCoupons.length - 1; j >= 0; j--) {
                    if (uCoupons[j].UseThisCouponProductIdList.includes(products[i].pid)) { // 该指定商品固定金额代金券运用在本商品上
                        tempCouponCategoryIds += uCoupons[j].CouponCategoryId + "|1;";
                        //myProductCouponTotalPrice += uCoupons[j].FactOffSetMoney;
                        couponMoney += uCoupons[j].FactOffSetMoney;
                        myCouponIds += uCoupons[j].CouponId + "|";
                        couponNum++;

                        t_getIntegrationValue -= products[i].getIntegrationValue;

                        if (uCoupons[j].IsGeneralCommon === false) {
                            if (uCoupons[j].MemberDiscountCanUse) {
                                products[i].vipprice = products[i].vipprice || 0;
                                t_vipPrice += products[i].orgprice - products[i].vipprice;
                                totalPrice += products[i].vipprice;
                            } else { // 不允许使用会员折扣
                                products[i].vipprice = products[i].orgprice;
                                totalPrice += products[i].orgprice;
                            }
                        } else {
                            products[i].vipprice = products[i].vipprice || 0;
                            t_vipPrice += products[i].orgprice - products[i].vipprice;
                            totalPrice += products[i].vipprice;
                        }
                        
                        uCoupons.splice(j, 1); // 移除已经使用过的券
                        products.splice(i, 1);// 移除已经用过券的商品
                        break;
                    }
                }

            }
        }

        for (var i = 0; i < products.length; i++) {
            products[i].vipprice = products[i].vipprice || 0;
            t_vipPrice += products[i].orgprice - products[i].vipprice;
            if (products[i].vipprice == 0) {
                totalPrice += products[i].orgprice;
            } else {
                totalPrice += products[i].vipprice;
            }
        }

    }
    // 使用指定商品的折扣代金券和全场折扣优惠券
    else if (chosedCouponCase === "LimitDiscountCoupon" || chosedCouponCase === "UniversalDiscountCoupon") {
        t_vipPrice = 0;
        var coupon_unitDiscountPrice = {}; // 券-用券折扣价格值
        var products = JSON.parse(JSON.stringify(productList));
        for (var i = products.length - 1; i >= 0; i--) {
            var isRemoveThisProduct = false;
            $.each(coupons, function (index, coupon) {
                if (String(coupon.State) == "1" && String(coupon.Category) == "2") { //&& String(coupon.IsGeneralCommon) == 'false') {
                    // 判断此商品是否应用于本券
                    if (coupon.UseThisCouponProductIdList.includes(products[i].pid) && products[i].spec === 'Single') { // 适用
                        isRemoveThisProduct = true;
                        var s_totalPrice = 0; // 用券后的商品总价
                        var s_discountPrice = 0;// 用券折扣了多少钱
                        var s_factPrice = 0;

                        products[i].vipprice = products[i].vipprice || 0;
                        if ((products[i].isVipAndAgentWine && coupon.BuyOneFreeOneCanUse) || coupon.MemberDiscountCanUse) { //独代酒款或者可以享受会员折扣价格
                            t_vipPrice += (products[i].orgprice - products[i].vipprice) * products[i].quantity;
                            if (products[i].vipprice != 0) {
                                s_totalPrice = products[i].vipprice * products[i].quantity;
                            } else {
                                s_totalPrice = products[i].orgprice * products[i].quantity;
                            }
                        } else {
                            s_totalPrice = products[i].orgprice * products[i].quantity;
                        }
                        // 计算折扣
                        if (s_totalPrice * (10 - coupon.HighDiscount) != 0) {
                            s_discountPrice = s_totalPrice * (10 - coupon.HighDiscount) / 10;
                            if (s_discountPrice > coupon.HighMoney) {
                                s_discountPrice = coupon.HighMoney;
                            }
                        }

                        // 校验该券是否达到了最大优惠值(指定商品的折扣券可以同时应用于几个不同的商品)
                        if (typeof (coupon_unitDiscountPrice[coupon.CouponId]) == "undefined") {
                            coupon_unitDiscountPrice[coupon.CouponId] = s_discountPrice;

                            tempCouponCategoryIds += coupon.CouponCategoryId + "|1;";
                            myCouponIds += coupon.CouponId + "|";
                            couponNum++;
                        } else {
                            if (coupon_unitDiscountPrice[coupon.CouponId] + s_discountPrice > coupon.HighMoney) {
                                s_discountPrice = coupon.HighMoney - coupon_unitDiscountPrice[coupon.CouponId];
                                coupon_unitDiscountPrice[coupon.CouponId] = coupon.HighMoney;
                            } else {
                                coupon_unitDiscountPrice[coupon.CouponId] += s_discountPrice;
                            }
                        }

                        s_factPrice = s_totalPrice - s_discountPrice;

                        c_discountMoney += s_discountPrice;
                        totalPrice += s_totalPrice;

                        t_getIntegrationValue -= products[i].getIntegrationValue * products[i].quantity;
                    }
                }
            });
            if (isRemoveThisProduct) {
                products.splice(i, 1); //移除已经用过券的商品
            }
        }


        for (var i = 0; i < products.length; i++) {// 剩下没有用券的商品进行遍历
            t_vipPrice += (products[i].orgprice - products[i].vipprice) * products[i].quantity;
            var s_totalPrice = products[i].vipprice * products[i].quantity;
            totalPrice += s_totalPrice;
        }

        //myProductCouponTotalPrice = c_discountMoney;
        couponMoney = c_discountMoney;

    }
    // 指定商品满减和全场满减优惠券
    else if (chosedCouponCase === "LimitFullReduceCoupon" || chosedCouponCase === "UniversalFullReduceCoupon") {
        t_vipPrice = 0;
        var products = JSON.parse(JSON.stringify(productList));
        $.each(coupons, function (index, coupon) {
            var productsMoneys = 0;
            if (String(coupon.State) == "1" && String(coupon.Category) == "3") { //&& String(coupon.IsGeneralCommon) == 'false') {

                for (var i = products.length - 1; i >= 0; i--) {
                    var isRemoveThisProduct = false;
                    // 判断此商品是否应用于本券
                    if (coupon.UseThisCouponProductIdList.includes(products[i].pid) && products[i].spec === 'Single') { // 适用
                        isRemoveThisProduct = true;
                        // 用券后的商品总价
                        // 用券折扣了多少钱
                        var s_totalPrice = 0;
                        products[i].vipprice = products[i].vipprice || 0;
                        if ((products[i].isVipAndAgentWine && coupon.BuyOneFreeOneCanUse) || coupon.MemberDiscountCanUse) { //独代酒款或者可以享受会员折扣价格
                            t_vipPrice += (products[i].orgprice - products[i].vipprice) * products[i].quantity;
                            if (products[i].vipprice != 0) {
                                s_totalPrice = products[i].vipprice * products[i].quantity;
                            } else {
                                s_totalPrice = products[i].orgprice * products[i].quantity;
                            }
                        } else {
                            s_totalPrice = products[i].orgprice * products[i].quantity;
                        }
                        t_getIntegrationValue -= products[i].getIntegrationValue * products[i].quantity;
                        productsMoneys += s_totalPrice;
                        totalPrice += s_totalPrice;
                    }
                    if (isRemoveThisProduct) {
                        products.splice(i, 1); //移除已经用过券的商品
                    }
                }
                //判断指定商品总金额是否达到满减券使用要求 
                if (productsMoneys >= coupon.FullMoney) {
                    c_discountMoney += coupon.ReduceMoney;
                    tempCouponCategoryIds += coupon.CouponCategoryId + "|1;";
                    myCouponIds += coupon.CouponId + "|";
                   // UpDateMyCouponIdsValue(myCouponIds);
                    couponNum++;
                }

            }
        });


        for (var i = 0; i < products.length; i++) {// 剩下没有用券的商品进行遍历
            products[i].vipprice = products[i].vipprice || 0;
            //if (chosedCouponCase == "UniversalFullReduceCoupon") {
            //    products[i].vipprice = products[i].orgprice;
            //}

            t_vipPrice += (products[i].orgprice - products[i].vipprice) * products[i].quantity;

            var s_totalPrice = 0;
            if (products[i].vipprice == 0) {
                s_totalPrice = products[i].orgprice * products[i].quantity;
            } else {
                s_totalPrice = products[i].vipprice * products[i].quantity;
            }
            totalPrice += s_totalPrice;
        }

        //myProductCouponTotalPrice = c_discountMoney;
        couponMoney = c_discountMoney;
    }
    else {
        t_vipPrice = 0;
        totalPrice = 0;
        for (var i = 0; i < productList.length; i++) {
            t_vipPrice += (productList[i].orgprice - productList[i].vipprice) * productList[i].quantity;
            var s_totalPrice = productList[i].vipprice * productList[i].quantity;
            totalPrice += s_totalPrice;
        }
        couponMoney = 0;
        //myProductCouponTotalPrice = 0;
    }


    price = totalPrice;
    myProductCouponTotalPrice = couponMoney;
    myCouponCategoryId_Count_Info = tempCouponCategoryIds;

    orderData.vipDiscountPrice = t_vipPrice;
    orderData.gainTotalZMJF = t_getIntegrationValue;
    orderData.productCoupon.count = couponNum;
    orderData.productCoupon.couponDiscountPrice = myProductCouponTotalPrice;

    UpdateByMyCoupon();
    UpdateOrderData();
}

/**
 * 数据变动时更新
 */
function UpdateOrderData() {

    var originTotalPrice =(orderData.originTotalPrice * 100 + orderData.tradeInService.totalPrice * 100) / 100;
    var finalTotalPrice = GetFinalTotalPrice();

    orderData.finalTotalPrice = finalTotalPrice;

    var payTotalZMJF = orderData.payTotalZMJF + orderData.tradeInService.payZMJF;
    var totalCount = orderData.totalCount + orderData.tradeInService.count;

    changeOriginTotalPayPrice(originTotalPrice.toFixed(2));
    changePayprice(finalTotalPrice.toFixed(2));

    orderData.fullFreePrice = orderData.fullFreePrice < 0 ? 0 : orderData.fullFreePrice;
    $("#fullFreePrice_int").text(orderData.fullFreePrice.toFixed(2).split('.')[0]);
    $("#fullFreePrice_float").text(orderData.fullFreePrice.toFixed(2).split('.')[1]);
    if (orderData.fullFreePrice > 0) {
        $("#displayFullFreePrice").show();
    } else {
        $("#displayFullFreePrice").hide();
    }

    orderData.fullDiscountPrice = orderData.fullDiscountPrice < 0 ? 0 : orderData.fullDiscountPrice;
    $("#fullDiscountPrice_int").text(orderData.fullDiscountPrice.toFixed(2).split('.')[0]);
    $("#fullDiscountPrice_float").text(orderData.fullDiscountPrice.toFixed(2).split('.')[1]);
    if (orderData.fullDiscountPrice > 0) {
        $("#displayFullDiscountPrice").show();
    } else {
        $("#displayFullDiscountPrice").hide();
    }

    orderData.vipDiscountPrice = orderData.vipDiscountPrice < 0 ? 0 : orderData.vipDiscountPrice;
    $("#vipTotalDiscount_int").text(orderData.vipDiscountPrice.toFixed(2).split('.')[0]);
    $("#vipTotalDiscount_float").text(orderData.vipDiscountPrice.toFixed(2).split('.')[1]);
    if (orderData.vipDiscountPrice > 0) {
        $("#vipTotalDiscount").show();
    } else {
        $("#vipTotalDiscount").hide();
    }

    orderData.productCoupon.couponDiscountPrice = orderData.productCoupon.couponDiscountPrice < 0 ? 0 : orderData.productCoupon.couponDiscountPrice;
    $("#productCoupon_int").text(orderData.productCoupon.couponDiscountPrice.toFixed(2).split('.')[0]);
    $("#productCoupon_float").text(orderData.productCoupon.couponDiscountPrice.toFixed(2).split('.')[1]);
    $("#couponMoney").text(orderData.productCoupon.couponDiscountPrice.toFixed(2));
    $("#couponNum").text(orderData.productCoupon.count);
    if (orderData.productCoupon.couponDiscountPrice > 0) {
        $("#disMyProductCoupon").show();
    } else {
        $("#disMyProductCoupon").hide();
    }

    orderData.zmCoupon.pay = orderData.zmCoupon.pay < 0 ? 0 : orderData.zmCoupon.pay;
    $("#couponPrice").text(orderData.zmCoupon.pay.toFixed(2).split('.')[0]);
    $("#couponPrice_float").text(orderData.zmCoupon.pay.toFixed(2).split('.')[1]);
    $("#txtZMcouPon").val(orderData.zmCoupon.pay.toFixed(2).split('.')[0]);
    $("#spanCouponMoney").text(orderData.zmCoupon.pay.toFixed(2).split('.')[0]);
    if (orderData.zmCoupon.pay > 0) {
        $("#disCoupon").show();
    } else {
        $("#disCoupon").hide();
    }

    orderData.wineCoupon.pay = orderData.wineCoupon.pay < 0 ? 0 : orderData.wineCoupon.pay;
    $("#wineCouponPrice").text(orderData.wineCoupon.pay.toFixed(2).split('.')[0]);
    $("#wineCouponPrice_float").text(orderData.wineCoupon.pay.toFixed(2).split('.')[1]);
    $("#txtWinecouPon").val(orderData.wineCoupon.pay.toFixed(2).split('.')[0]);
    $("#spanWineCouponMoney").text(orderData.wineCoupon.pay.toFixed(2).split('.')[0]);
    if (orderData.wineCoupon.pay > 0) {
        $("#disWineCoupon").show();
    } else {
        $("#disWineCoupon").hide();
    }

    orderData.wineWorldCoupon.pay  = orderData.wineWorldCoupon.pay < 0 ? 0 : orderData.wineWorldCoupon.pay; 
    $("#wineWorldCouponPrice").text(orderData.wineWorldCoupon.pay.toFixed(2).split('.')[0]);
    $("#wineWorldCouponPrice_float").text(orderData.wineWorldCoupon.pay.toFixed(2).split('.')[1]);
    $("#txtWineWorldCoupon").val(orderData.wineWorldCoupon.pay.toFixed(2).split('.')[0]);
    $("#spanWineWorldCouponMoney").text(orderData.wineWorldCoupon.pay.toFixed(2).split('.')[0]);
    if (orderData.wineWorldCoupon.pay > 0) {
        $("#disWineWorldCoupon").show();
    } else {
        $("#disWineWorldCoupon").hide();
    }

    orderData.gainTotalZMJF = orderData.gainTotalZMJF < 0 ? 0 : orderData.gainTotalZMJF;
    $("#userjf_val").text(orderData.gainTotalZMJF);
    if (orderData.gainTotalZMJF > 0 ) {
        $(".userjf").show();
    } else {
        $(".userjf").hide();
    }

    $("#payZMJF").text(payTotalZMJF);
    if (payTotalZMJF > 0) {
        $("#disPayZMJF").show();
    } else {
        $("#disPayZMJF").hide();
    }
    
}

function GetFinalTotalPrice() {

    var originTotalPrice = (orderData.originTotalPrice * 100 + orderData.tradeInService.totalPrice * 100) / 100;

    var finalTotalPrice = (originTotalPrice * 100 - orderData.vipDiscountPrice * 100 - orderData.fullFreePrice * 100 - orderData.fullDiscountPrice * 100 -
        orderData.wineCoupon.pay * 100 - orderData.wineWorldCoupon.pay * 100 - orderData.zmCoupon.pay * 100 - orderData.productCoupon.couponDiscountPrice * 100) / 100;

    return finalTotalPrice;
}

function UpdateByMyCoupon() {

    var originTotalPrice = (orderData.originTotalPrice * 100 + orderData.tradeInService.totalPrice * 100)/100;
    var tempPrice = (originTotalPrice * 100 - orderData.vipDiscountPrice * 100 - orderData.fullFreePrice * 100 - orderData.fullDiscountPrice * 100 -
        orderData.wineCoupon.pay * 100 - orderData.wineWorldCoupon.pay * 100 - orderData.zmCoupon.pay * 100)/100;

    var maxAllow = orderData.productCoupon.couponDiscountPrice < tempPrice ? orderData.productCoupon.couponDiscountPrice : tempPrice;

    if (orderData.productCoupon.couponDiscountPrice != 0 && maxAllow <= 0) {
        $("#txtZMcouPon").val(0);
        $("#txtWinecouPon").val(0);
        $("#txtWineWorldCoupon").val(0);
        orderData.zmCoupon.pay = 0;
        orderData.wineCoupon.pay = 0;
        orderData.wineWorldCoupon.pay = 0;
        $("#spanCouponMoney").text(0);
        $("#spanWineCouponMoney").text(0);
        $("#spanWineWorldCouponMoney").text(0);

        $("#disWineWorldCoupon").hide();
        $("#disCoupon").hide();
        $("#disWineCoupon").hide();
    }
    if (orderData.productCoupon.couponDiscountPrice > tempPrice) {
        orderData.productCoupon.couponDiscountPrice = maxAllow;
    }

    return;
    
    AllJiFenChange();
}

/**
 * 计算满减和满免价格 
 */
function updateFreePrice() {
  
    orderData.fullFreePrice = parseFloat($("#temp_FullFreePrice").val());
    orderData.fullDiscountPrice = parseFloat($("#temp_FullDiscountPrice").val());
    orderData.totalFareCartsPrice = parseFloat($("#hid_totalFareCartsPrice").val());
}

// 修改订单应付总价
function changePayprice(value) {

    $(".spanPay_int").text(value.split('.')[0]);
    $(".spanPay_decimal").text('.' + value.split('.')[1]);

    var totalCount = orderData.totalCount + orderData.tradeInService.count;
    $("#order_toatalCount").text(totalCount);
}
// 修改订单原始总价
function changeOriginTotalPayPrice(value) {
    $("#spanPay-u").text(value.split('.')[0]);
    $("#spanPay_total_decimal").text('.' + value.split('.')[1]);
}

function AllJiFenChange() {

    $("#txtWineWorldCoupon").blur();

    $("#txtZMcouPon").blur();

    $("#txtWinecouPon").blur();
}

//跨境电商不允许使用中民积分，代金券
function GetCrossTotalPrice() {
    var crossTotalPrice = 0;
    if ($("#CrossTotalPrice").length > 0) {
        crossTotalPrice = parseFloat($("#CrossTotalPrice").val()).toFixed(1);
    }
    return crossTotalPrice;
}

//---代金券相关 END--------
