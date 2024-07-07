$(document).ready(function () {
    var successMessage = $("#jq-notification");
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        var book_id = $(this).data("book-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                book_id: book_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                if (!data.message.includes("вже було додано до кошику") && !data.message.includes("немає в наявності") 
                && !data.message.includes("Ви не є читачем")) {
                    cartCount++;
                    goodsInCartCount.text(cartCount);
                }
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },

            error: function (data) {
                console.log("Add error");
            },
        });
    });

    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        var cart_id = $(this).data("cart-id");
        var remove_from_cart = $(this).attr("href");
    
        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                if (!data.message.includes("Ви не є читачем")) {
                    cartCount -= data.quantity_deleted;
                    goodsInCartCount.text(cartCount);
                }
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },

            error: function (data) {
                console.log("Remove error");
            },
        });
    });

    $(document).ready(function () {
        $(document).on("click", ".watch-pdf-link", function (e) {
            e.preventDefault();
    
            var bookId = $(this).data("book-id");
            var controllerUrl = $(this).data("controller-url");
            var pdfLink = $(this).attr("href");
    
            $.ajax({
                type: "POST",
                url: controllerUrl,
                data: {
                    book_id: bookId,
                    csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                },
                success: function (data) {
                    if (data.success) {
                        window.open(pdfLink, "_blank");
                    } else {
                        window.open(pdfLink, "_blank");
                        console.log("Watched link already exists");
                    }
                },
                error: function (data) {
                    console.log("Error sending POST request to check_watched_link");
                },
            });
        });
    });    

    $(document).on("click", ".edit-comment", function (e) {
        e.preventDefault();

        var commentId = $(this).data("comment-id");
        if ($("#comment-text-" + commentId).hasClass("d-none")) {
            $("#comment-text-" + commentId).removeClass("d-none");
            $("#edit-comment-form-" + commentId).addClass("d-none");
        } else {
            $("#comment-text-" + commentId).addClass("d-none");
            $("#edit-comment-form-" + commentId).removeClass("d-none");
        }
    });
    
    $(document).ready(function () {
        const loadMoreBtn = document.getElementById('load-more');
        const commentSection = document.getElementById('comment-section');
        const commentsContainer = document.getElementById('comments-container');
        if (loadMoreBtn && commentsContainer && commentSection) {
            const comments = commentsContainer.querySelectorAll('.comment');
            console.log(comments)
            const totalComments = comments.length;
            const commentsPerPage = 3;
            let visibleComments = commentsPerPage;

            comments.forEach(function(comment, index) {
                if (index >= commentsPerPage) {
                    comment.classList.add('d-none');
                    const hrLine = commentSection.querySelectorAll('hr')[index];
                    if (hrLine) {
                        hrLine.classList.add('d-none');
                    }
                }
            });

            loadMoreBtn.addEventListener('click', function() {
                visibleComments += commentsPerPage;
                comments.forEach(function(comment, index) {
                    if (index < visibleComments) {
                        comment.classList.remove('d-none');
                        const hrLine = commentSection.querySelectorAll('hr')[index];
                        if (hrLine) {
                            hrLine.classList.remove('d-none');
                        }
                    }
                });
                if (visibleComments >= totalComments) {
                    loadMoreBtn.classList.add('d-none');
                }
            });
        }
    });

    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    $("input[name='requires_delivery']").change(function() {
        var selectedValue = $(this).val();
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });
});

$(document).ready(function () {
    function checkFooterPosition() {
        var scroll = window.innerHeight < document.body.scrollHeight;
        var footer = document.querySelector('footer');
        if (scroll) {
            footer.classList.remove('fixed-bottom');
        } else {
            footer.classList.add('fixed-bottom');
        }
    }
    checkFooterPosition();
    window.addEventListener('resize', checkFooterPosition);

    var curr_time = new Date().getHours();
    var greeting_section = document.getElementById("greetingHeading");

    if (curr_time >= 5 && curr_time < 12) {
        greeting_section.innerHTML = "Добрий ранок";
    } else if (curr_time >= 12 && curr_time < 18) {
        greeting_section.innerHTML = "Добрий день";
    } else {
        greeting_section.innerHTML = "Добрий вечір";
    }
});

$(document).ready(function () {
    const ratingContainers = document.querySelectorAll('.rating-container');
    ratingContainers.forEach(container => {
        container.addEventListener('mouseenter', () => {
            const helpIcon = container.querySelector('.rating-help-icon');
            helpIcon.style.animation = 'showIcon 0.3s ease-in-out';
        });
    });
});
