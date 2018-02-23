 var fadeTime = 300;

//Search
function tampilCari() {document.getElementById('search-nav').setAttribute("class", "search-nav-click");}
function tutupCari() {document.getElementById('search-nav').setAttribute("class", "search-nav");} 
 
// Form Select
$(document).ready(function() {
    $('select').material_select();
});
        

//Navbar Menu Mobile
$('.button-collapse').sideNav({
    edge: 'left', // Choose the horizontal origin
    menuWidth: '80%'
  }
);

$(document).ready(function(){
  $('ul.tabs').tabs();
});

// Tabs
$(document).ready(function(){
    $('ul.tabs').tabs();
});

//Progress Bar - Carousel
$(document).ready(function(){
      var percent = 0, bar = $('.transition-timer-carousel-progress-bar'), crsl = $('#myCarousel');
			function progressBarCarousel() {
			  bar.css({width:percent+'%'});
			 percent = percent +0.5;
			  if (percent>100) {
			      percent=0;
			      crsl.carousel('next');
			  }      
			}
			crsl.carousel({
			    interval: false,
			    pause: true
			}).on('slid.bs.carousel', function () {});var barInterval = setInterval(progressBarCarousel, 30);
			crsl.hover(
			    function(){
			        clearInterval(barInterval);
			    },
			    function(){
			        barInterval = setInterval(progressBarCarousel, 30);
          })
 });
 
 //Gallery Slider
$('.gallery-agro').owlCarousel({
    margin:15,
    responsiveClass:true,
    autoplay:false,
	autoWidth:true,
    nav:false,
})

 //Product Detail Image
$('.detail-product-img').owlCarousel({
    margin:24,
    responsiveClass:true,
    autoplay:false,
    nav:false,
    responsive:{
        0:{
            items:1,
        },
        601:{
            items:1,
        },
        993:{
            items:1,
        },
        1201:{
            items:1,
        }
    }
})

//Other Product Slide
$('.other-product-slide').owlCarousel({
    margin:24,
    responsiveClass:true,
    autoplay:false,
    nav:false,
    responsive:{
        0:{
            items:1,
        },
        601:{
            items:3,
        },
        993:{
            items:3,
        },
        1201:{
            items:3,
        }
    }
})

//Product Slider
$('.product-slide').owlCarousel({
    margin:24,
    responsiveClass:true,
    autoplay:true,
    autoplayTimeout:7000,
    autoplayHoverPause:true,
    nav:false,
    responsive:{
        0:{
            items:1,
        },
        601:{
            items:2,
        },
        993:{
            items:3,
        },
        1201:{
            items:4,
        }
    }
})

// Main Slider
$(document).ready(function(){
  var time = 2;
  var $bar,
      $slick,
      isPause,
      tick,
      percentTime;
  
  $slick = $('.slider');
  $slick.slick({
    draggable: true,
    adaptiveHeight: false,
    dots: true,
    mobileFirst: true,
    pauseOnDotsHover: true,
  });
  
  $bar = $('.slider-progress .progress');
  
  $('.slider-wrapper').on({
    mouseenter: function() {
      isPause = true;
    },
    mouseleave: function() {
      isPause = false;
    }
  })
  
  function startProgressbar() {
    resetProgressbar();
    percentTime = 0;
    isPause = false;
    tick = setInterval(interval, 25);
  }
  
  function interval() {
    if(isPause === false) {
      percentTime += 1 / (time+0.1);
      $bar.css({
        width: percentTime+"%"
      });
      if(percentTime >= 100)
        {
          $slick.slick('slickNext');
          startProgressbar();
        }
    }
  }
  
  
  function resetProgressbar() {
    $bar.css({
     width: 0+'%' 
    });
    clearTimeout(tick);
  }
  
  startProgressbar();
  
});

//Shopping Cart
/* Set rates + misc */
var uniqueRate = 734;

/* Assign actions */
$('.product-quantity input').change( function() {
  updateQuantity(this);
});

$('.product-removal img').click( function() {
  removeItem(this);
});


/* Recalculate cart */
function recalculateCart()
{
  var subtotal = 0;
  
  /* Sum up row totals */
  $('.product-detail').each(function () {
    subtotal += parseFloat($(this).children('.product-line-price').text());
  });
  
  /* Calculate totals */
  var unique = (subtotal > 0 ? uniqueRate : 0);
  var total = subtotal + unique;
  
  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function() {
    $('#cart-subtotal').html(subtotal);
    $('#cart-unique').html(unique);
    $('#cart-total').html(total);
    if(total == 0){
      $('.fill-cart').fadeOut(fadeTime);
      $('.empty-cart').fadeIn(fadeTime);
    }else{
      $('.fill-cart').fadeIn(fadeTime);
      $('.empty-cart').fadeOut(fadeTime);
    }
    $('.totals-value').fadeIn(fadeTime);
  });
}


/* Update quantity */
function updateQuantity(quantityInput)
{
  /* Calculate line price */
  var productRow = $(quantityInput).parent().parent();
  var price = parseFloat(productRow.children('.product-price').text());
  var quantity = $(quantityInput).val();
  var linePrice = price * quantity;
  
  /* Update line price display and recalc cart totals */
  productRow.children('.product-line-price').each(function () {
    $(this).fadeOut(fadeTime, function() {
      $(this).text(linePrice);
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });  
}

/* Remove item from cart */
function removeItem(removeButton)
{
  /* Remove row from DOM and recalc cart total */
  var productRow = $(removeButton).parent().parent().parent().parent();
  productRow.slideUp(fadeTime, function() {
    productRow.remove();
    recalculateCart();
  });
}

//Review Show
$(document).ready(function(){
    $("#closeReview").click(function(){
        $("#review-form").slideUp(fadeTime);
    });
    $("#openReview").click(function(){
        $("#review-form").slideDown(fadeTime);
    });
});

//Another Address
function anotherAddress()
{
    if($('.another-address-btn').is(":checked"))   
        $(".another-address").slideDown(fadeTime);
    else
        $(".another-address").slideUp(fadeTime);
}

//Copy to Clipboard
function copyToClipboard(element) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  $temp.remove();
}

//Drag Drop Upload
var dropzone = new Dropzone('#transfer-proof', {
  previewTemplate: document.querySelector('#preview-template').innerHTML,
  parallelUploads: 2,
  thumbnailHeight: 120,
  thumbnailWidth: 120,
  maxFilesize: 3,
  filesizeBase: 1000,
  thumbnail: function(file, dataUrl) {
    if (file.previewElement) {
      file.previewElement.classList.remove("dz-file-preview");
      var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
      for (var i = 0; i < images.length; i++) {
        var thumbnailElement = images[i];
        thumbnailElement.alt = file.name;
        thumbnailElement.src = dataUrl;
      }
      setTimeout(function() { file.previewElement.classList.add("dz-image-preview"); }, 1);
    }
  }

});


// Now fake the file upload, since GitHub does not handle file uploads
// and returns a 404

var minSteps = 6,
    maxSteps = 60,
    timeBetweenSteps = 100,
    bytesPerStep = 100000;

dropzone.uploadFiles = function(files) {
  var self = this;

  for (var i = 0; i < files.length; i++) {

    var file = files[i];
    totalSteps = Math.round(Math.min(maxSteps, Math.max(minSteps, file.size / bytesPerStep)));

    for (var step = 0; step < totalSteps; step++) {
      var duration = timeBetweenSteps * (step + 1);
      setTimeout(function(file, totalSteps, step) {
        return function() {
          file.upload = {
            progress: 100 * (step + 1) / totalSteps,
            total: file.size,
            bytesSent: (step + 1) * file.size / totalSteps
          };

          self.emit('uploadprogress', file, file.upload.progress, file.upload.bytesSent);
          if (file.upload.progress == 100) {
            file.status = Dropzone.SUCCESS;
            self.emit("success", file, 'success', null);
            self.emit("complete", file);
            self.processQueue();
            //document.getElementsByClassName("dz-success-mark").style.opacity = "1";
          }
        };
      }(file, totalSteps, step), duration);
    }
  }
}

//Booking Calendar
$(document).ready(function() {

    // page is now ready, initialize the calendar..
    $('#calendar').fullCalendar({
        weekends: false,
        dayClick: function() {
          alert('a day has been clicked!');
        },
        defaultView: 'month'
        
    });
  


});
  