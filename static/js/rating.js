/**
 * Created by sherali on 12/15/15.
 */

$(document).ready(function () {
    $.fn.rating = function (options) {
        //settings
        var settings = $.extend({}, $.fn.rating.defaultOptions, options);
        var R = {
            initialize: function (wrapper) {
                this.dom.wrapper.tagName = wrapper;
                this.createDOMElements();

                this.attachHandlers();

                return this;
            },

            createDOMElements: function () {
                this.dom.wrapper.tagName.html("");
                this.dom.wrapper.tagName.addClass(this.dom.wrapper.className);
                this.dom.wrapper = this.dom.wrapper.tagName;

                this.dom.list = this.appendDOMElement(this.dom.list);
                this.dom.wrapper.append(this.dom.list);


                this.dom.footer = this.appendDOMElement(this.dom.footer);
                this.dom.wrapper.append(this.dom.footer);

                this.dom.min = this.appendDOMElement(this.dom.min);
                this.dom.min.text(settings.minString);
                this.dom.min.addClass("info");
                this.dom.footer.append(this.dom.min);

                this.dom.max = this.appendDOMElement(this.dom.max);
                this.dom.max.text(settings.maxString);
                this.dom.max.addClass("info");
                this.dom.footer.append(this.dom.max);

                for (var i = 0; i < this.itemCount; i++) {
                    var tempItem = this.appendDOMElement(this.dom.item);
                    tempItem.html(this.innerItem);
                    tempItem.addClass(i);
                    tempItem.attr("data-index", i);

                    this.dom.list.append(tempItem);
                    this.dom.list.append(" ");
                }
            },

            attachHandler: function (element, handler, eventType, options) {
                eventType = eventType || 'click';

                if (typeof element == "string") {
                    R.documentBody.on(eventType, element, handler);
                } else {
                    $(element).on(eventType, handler);
                }
            },

            attachHandlers: function () {
                var lastIndex = R.activeIndex, hoverIndex = -1;
                R.dom.list.find("li:gt(" + (lastIndex) + ")").removeClass("hovered");
                R.dom.list.find("li:lt(" + (lastIndex + 1) + ")").addClass("hovered");

                if ($.isFunction(settings.complete)) {
                    settings.complete.call(R, (lastIndex + 1));
                }

                R.attachHandler("." + R.dom.item.className, function (ev) {
                    var index = parseInt($(this).attr("data-index"));
                    if (hoverIndex == index) return;
                    hoverIndex = index;

                    R.dom.list.find("li:lt(" + (index + 1) + ")").addClass("hovered");
                    R.dom.list.find("li:gt(" + (index ) + ")").removeClass("hovered");
                }, "mouseover");

                R.attachHandler(R.dom.list, function (ev) {
//                    if (index == lastIndex) return;
//                    $(this)
//                        .children()
//                        .removeClass("hovered");
                    if (lastIndex !== -1) {
                        R.dom.list.find("li:gt(" + (lastIndex) + ")").removeClass("hovered");
                        R.dom.list.find("li:lt(" + (lastIndex + 1) + ")").addClass("hovered");
                    } else {
                        R.dom.list.children().removeClass("hovered");
                    }
                    hoverIndex = lastIndex;
                }, "mouseleave");

                R.attachHandler("." + R.dom.item.className, function (ev) {
                    var index = parseInt($(this).attr("data-index"));
                    if (index)
                        R.dom.list.find("li:lt(" + (index + 1) + ")").addClass("hovered");
                    R.dom.list.find("li:gt(" + (index + 1) + ")").removeClass("hovered");
                    lastIndex = index;
                    if ($.isFunction(settings.complete)) {
                        settings.complete.call(R, (index + 1));
                    }
                }, "click touchstart");

            },

            appendDOMElement: function (dom) {
                var option = {class: dom.className};
                switch (dom.tagName) {
                    case "span":
                    case "div":
                    case "i":
                        break;
                    case "input":
                        option.type = "text";
                        break;
                }
                return $("<" + dom.tagName + "/>", option);
            },

            documentBody: $('body'),
            dom: {
                wrapper: {
                    tagName: "div",
                    className: "rating-box"
                },
                list: {
                    tagName: "ul",
                    className: "item-list"
                },
                item: {
                    tagName: "li",
                    className: "rating-item"
                },
                footer: {
                    tagName: "div",
                    className: "footer"
                },
                min: {
                    tagName: "span",
                    className: "min"
                },
                max: {
                    tagName: "span",
                    className: "max"
                },
                total: {
                    tagName: "span",
                    className: "rating-result"
                }
            },
            width: null,
            searchKey: "",
            itemCount: settings.itemCount,
            innerItem: settings.innerItem,
            activeIndex: (settings.activeIndex - 1)
        };

        return R.initialize($(this));
    };

    $.fn.rating.defaultOptions = {
        placeholder: "Tegni kiriting!",
        itemCount: 5,
        minString: "Bad",
        maxString: "Great",

        activeIndex: 0,
        innerItem: "<i class='fa fa-star'></i>",
        complete: null,//function
        load: null,//function
    };
});