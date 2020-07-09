$(document).ready(function () {

        let images = $('.product-details-gallery-image img');

        images.each(function () {
            $(this).click(function () {
                let display = $('.product__details__pic__item--large');
                display.attr('src', $(this).attr('src'));

            })
        })

        let btnAddFavourite = $('.add_favourite');

        btnAddFavourite.each(function () {

            $(this).click(function () {

                $.ajax({
                    url: '/produkt/ulubione/dodaj_usun/'+$(this).children(":first").val(),
                    dataType: 'json',
                    success: function() {
                            alert("Udało się!");
                    }
                });

                console.log($(this).parents('li').css('display', 'none'));

            })
        })

        let btnRemoveFavourite = $('.remove_favourite');

        btnRemoveFavourite.each(function () {

            $(this).click(function () {

                $.ajax({
                    url: '/produkt/ulubione/dodaj_usun/'+$(this).children(":first").val(),
                    dataType: 'json',
                    success: function() {
                            alert("Udało się!");
                    }
                });

                console.log($(this).parents('tr').css('display', 'none'));

            })
        })

        let btnAddRemoveFavourite = $('.add_remove_favourite');

            btnAddRemoveFavourite.each(function () {
                $(this).click(function () {

                    if($(this).hasClass('icon_heart_alt')){
                        $(this).switchClass('icon_heart_alt', 'icon_heart');
                    }else{
                        $(this).switchClass('icon_heart', 'icon_heart_alt');
                    }

                    $.ajax({
                        url: '/produkt/ulubione/dodaj_usun/'+$(this).children(":first").val(),
                        dataType: 'json',
                        success: function() {
                                alert("Udało się!");
                        }
                    });

                })
            })







    })



