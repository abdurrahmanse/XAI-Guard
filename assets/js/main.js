(function ($) {
	"use strict";

  // Screen Width
var screen_width = window.screen.width;

 // Active GSAP
if (document.querySelector("#smooth-animate").classList.contains("smooth-scrool-animate")) {
  const smoother = ScrollSmoother.create({
      effects: screen_width < 1025 ? false : true,
      smooth: 1.35,
      ignoreMobileResize: true,
      normalizeScroll: false,
      smoothTouch: 0.1,
  });
}

var mySwiper = new Swiper('.swiper__container', {
  freeMode: true,
  slidesPerView: 'auto',
  spaceBetween: 60,
  scrollbar: {
    el: '.js-swiper-scrollbar',
    draggable: true,
    snapOnRelease: false
  }
});


/*------------------------------------------
        = CONTACT FORM SUBMISSION
    -------------------------------------------*/
    if ($("#contact-form-mejor").length) {
      $("#contact-form-mejor").validate({
          rules: {
              name: {
                  required: true,
                  minlength: 2
              },
              email: "required",
              phone: "required",
              subject: {
                  required: true
              }
          },
          messages: {
              name: "Please enter your name",
              email: "Please enter your email address",
              phone: "Please enter your phone number",
              subject: "Please select your contact subject"
          },
          submitHandler: function (form) {
              $.ajax({
                  type: "POST",
                  url: "mail-contact.php",
                  data: $(form).serialize(),
                  success: function () {
                      $("#loader").hide();
                      $("#success").slideDown("slow");
                      setTimeout(function () {
                          $("#success").slideUp("slow");
                      }, 3000);
                      form.reset();
                  },
                  error: function () {
                      $("#loader").hide();
                      $("#error").slideDown("slow");
                      setTimeout(function () {
                          $("#error").slideUp("slow");
                      }, 3000);
                  }
              });
              return false; // required to block normal submit since you used ajax
          }
      });
  }


// simpleParallax activation

var image = document.getElementsByClassName('imageParallax');
new simpleParallax(image, {
    delay: .5,
    transition: 'cubic-bezier(0,0,0,1)'
});


var image = document.getElementsByClassName('imageParallax2');
new simpleParallax(image, {
    delay: .6,
    transition: 'cubic-bezier(0,0,0,1)',
    orientation: 'right'
});
var image = document.getElementsByClassName('imageParallax3');
new simpleParallax(image, {
    delay: .6,
    transition: 'cubic-bezier(0,0,0,1)',
    orientation: 'left'
});


if (document.querySelector(".xlHeader--right")) {
  gsap.to('.xlHeader--right .xlHeader__header', {
    xPercent: -20,
    ease: "none",
    scrollTrigger: {
      trigger: ".xlHeader--right .xlHeader__header",
      start: "top center",
      end: "bottom top",
      scrub: true
    }
  });
}

if (document.querySelector(".xlHeader--left")) {
  gsap.to('.xlHeader--left .xlHeader__header', {
    xPercent: 20,
    ease: "none",
    scrollTrigger: {
      trigger: ".xlHeader--left .xlHeader__header",
      start: "top center",
      end: "bottom top",
      scrub: true,
    }
  });
}
 
const interleaveOffset = 0.75;

var swiper = new Swiper('.hero-slider2', {
  direction: 'vertical',
  speed: 800,
  mousewheelControl: true,
  watchSlidesProgress: true,
  mousewheel: {
    releaseOnEdges: true,
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: false,
    type: 'bullets',
    renderBullet: function (index, className) {
      return '<span class="' + className + '">' + ('0' + (index + 1)) + '</span>';
    }
  },
  on: {
    progress: function() {
      console.log('test')
      let swiper = this;

      for (let i = 0; i < swiper.slides.length; i++) {
        let slideProgress = swiper.slides[i].progress;
        let innerOffset = swiper.height * interleaveOffset;
        let innerTranslate = slideProgress * innerOffset;

        TweenMax.set(swiper.slides[i].querySelector(".slide-inner"), {
          y: innerTranslate,
        });
      }
    },
    setTransition: function(slider, speed) {
      let swiper = this;
      for (let i = 0; i < swiper.slides.length; i++) {
        swiper.slides[i].style.transition = speed + "ms";
        swiper.slides[i].querySelector(".slide-inner").style.transition =
          speed + "ms";
      }
    }
  }
});

const portfolio = new Swiper(".portfolio-slider", {
  loop: true,
  parallax: true,
  slidesPerView: 2,
  centeredSlides: false,
  spaceBetween: 30,
  initialSlide: 2,
});


  /*----------------------------
  testimonial
  ------------------------------ */ 
    $('.slider-for').slick({
      slidesToShow: 1,
      asNavFor: '.slider-nav',
      arrows: true,
      vertical: true,
      swipe:false
    });

    $('.slider-nav').slick({
      slidesToShow: 4,
      asNavFor: '.slider-for',
      dots: false,
      focusOnSelect: true,
      vertical: true,
      swipe:false
      
    });
/*--------------------------
testimonial-carousel 2
---------------------------- */
    $(".testimonial-carousel-2").slick({
      dots: false,
      arrows:true,
      slidesToShow: 1,
      slidesToScroll: 1,
      autoplay: true,
      prevArrow: '<i class="fa fa-angle-left"></i>',
      nextArrow: '<i class="fa fa-angle-right"></i>',
    });
    

    // Stacking Cards Js
    const cards = document.querySelectorAll(".stack-item");
    const stickySpace = document.querySelector(".stack-offset");
    const animation = gsap.timeline();
    let cardHeight;
    if (document.querySelector(".stack-item")) {
        function initCards() {
            animation.clear();
            cardHeight = cards[0].offsetHeight;
            //console.log("initCards()", cardHeight);
            cards.forEach((card, index) => {
                if (index > 0) {
                    gsap.set(card, { y: index * cardHeight });
                    animation.to(
                        card,
                        { y: 0, duration: index * 0.5, ease: "none" },
                        0
                    );
                }
            });
        }
        initCards();
        ScrollTrigger.create({
            trigger: ".stack-wrapper",
            start: "top top",
            pin: true,
            end: () => `+=${cards.length * cardHeight + stickySpace.offsetHeight}`,
            scrub: true,
            animation: animation,
            // markers: true,
            invalidateOnRefresh: true,
        });
        ScrollTrigger.addEventListener("refreshInit", initCards);
    }

	// Mobile Menu Js
	$("#main-menu").meanmenu({
		meanMenuContainer: "#mobile-navbar-menu",
		meanScreenWidth: "10000",
		meanExpand: ['<i class="fal fa-plus"></i>'],
	});
    

/*------------------------------------------------------
  /  Data js
  /------------------------------------------------------*/
  $("[data-bg-image]").each(function () {
    $(this).css(
      "background-image",
      "url(" + $(this).attr("data-bg-image") + ")"
    );
  });

  $("[data-bg-color]").each(function () {
    $(this).css("background-color", $(this).attr("data-bg-color"));
  });

 // Mobile Menu Overlay js
 var canva_expander = $(".canva_expander");
 if (canva_expander.length) {
    $(".canva_expander, #canva_close, #vw-overlay-bg").on("click", function (e) {
       e.preventDefault();
       $("body").toggleClass("canvas_expanded");
    });
 }

var swiper = new Swiper('.swiper-container', {
    slidesPerView: 1,
    speed: 800,
    parallax: true,
    loop: true,
    effect: 'fade',
    pagination:false,
    autoplay: false,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});

// DATA BACKGROUND IMAGE
var sliderBgSetting = $(".slide-bg-image");
sliderBgSetting.each(function(indx){
    if ($(this).attr("data-background")){
        $(this).css("background-image", "url(" + $(this).data("background") + ")");
    }
});

// Sticky js
$(window).scroll(function () {
  var Width = $(document).width();
  if ($("body").scrollTop() > 100 || $("html").scrollTop() > 100) {
      $(".header-sticky").addClass("sticky");
  } else {
      $(".header-sticky").removeClass("sticky");
  }
});


let marquee = document.querySelectorAll('.clipped-text');

// added event listener because it doesn't get the right width
addEventListener("load", function () {
 marquee.forEach(el => {
  // set a default rate, the higher the value, the faster it is
  let rate = 200;
  // get the width of the element
  let distance = el.clientWidth;
  // get the margin-right of the element
  let style = window.getComputedStyle(el);
  let marginRight = parseInt(style.marginRight) || 0;
  // get the total width of the element
  let totalDistance = distance + marginRight;
  // get the duration of the animation 
  // for a better explanation, see the quoted codepen in the first comment
  let time = totalDistance / rate;
  // get the parent of the element
  let container = el.parentElement;

  gsap.to(container, time, {
   repeat: -1,
   x: '-'+totalDistance,
   ease: Linear.easeNone,
  });
 });
});

// marquee
const init = () => {
    const marquee = document.querySelector('[wb-data="marquee"]');
    if (!marquee) {
      return;
    }
    const duration = parseInt(marquee.getAttribute("duration"), 10) || 5;
    console.log(duration);
    const marqueeContent = document.querySelector(".marquee-content");
    if (!marqueeContent) {
      return;
    }
  
    const marqueeContentClone = marqueeContent.cloneNode(true);
    marquee.append(marqueeContentClone);
  
    let tween;
  
    const playMarquee = () => {
      let progress = tween ? tween.progress() : 0;
      tween && tween.progress(0).kill();
      const width = parseInt(
        getComputedStyle(marqueeContent).getPropertyValue("width"),
        10
      );
  
      const gap = parseInt(
        getComputedStyle(marqueeContent).getPropertyValue("column-gap"),
        10
      );
  
      const distanceToTranslate = -1 * (gap + width);
  
      tween = gsap.fromTo(
        marquee.children,
        { x: 0 },
        { x: distanceToTranslate, duration, ease: "none", repeat: -1 }
      );
      tween.progress(progress);
    };
    playMarquee();
  
    function debounce(func) {
      var timer;
      return function (e) {
        if (timer) clearTimeout(timer);
        timer = setTimeout(
          () => {
            func();
          },
          500,
          e
        );
      };
    }
  
    window.addEventListener("resize", debounce(playMarquee));
  };
  
  document.addEventListener("DOMContentLoaded", init);

// ScrollTop js
var solarScrollTop = document.querySelector(".scroll-top");
if (solarScrollTop != null) {
    var scrollProgressPatch = document.querySelector(".scroll-top path");
    var pathLength = scrollProgressPatch.getTotalLength();
    var offset = 50;
    scrollProgressPatch.style.transition = scrollProgressPatch.style.WebkitTransition = "none";
    scrollProgressPatch.style.strokeDasharray = pathLength + " " + pathLength;
    scrollProgressPatch.style.strokeDashoffset = pathLength;
    scrollProgressPatch.getBoundingClientRect();
    scrollProgressPatch.style.transition = scrollProgressPatch.style.WebkitTransition = "stroke-dashoffset 10ms linear";
    window.addEventListener("scroll", function (event) {
        var scroll = document.body.scrollTop || document.documentElement.scrollTop;
        var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        var progress = pathLength - (scroll * pathLength) / height;
        scrollProgressPatch.style.strokeDashoffset = progress;
        var scrollElementPos = document.body.scrollTop || document.documentElement.scrollTop;
        if (scrollElementPos >= offset) {
        solarScrollTop.classList.add("progress-done");
        } else {
        solarScrollTop.classList.remove("progress-done");
        }
    });
    solarScrollTop.addEventListener("click", function (e) {
        e.preventDefault();
        window.scroll({
        top: 0,
        left: 0,
        behavior: "smooth",
        });
    });
}
    $(window).on("load", function () {
	// WoW Js
		var wow = new WOW({
			boxClass: "wow", // default
			animateClass: "animated", // default
			offset: 100, // default
			mobile: true, // default
			live: true, // default
		});
		wow.init();

        // Preloader Js
		const svg = document.getElementById("preloaderSvg");
		const svgText = document.querySelector(
			".hero-section .intro_text svg text"
		);
		const tl = gsap.timeline({
			onComplete: startStrokeAnimation,
		});
		const curve = "M0 502S175 272 500 272s500 230 500 230V0H0Z";
		const flat = "M0 2S175 1 500 1s500 1 500 1V0H0Z";

		tl.to(".preloader-heading .load-text , .preloader-heading .cont", {
			delay: 1.5,
			y: -100,
			opacity: 0,
		});
		tl.to(svg, {
			duration: 0.5,
			attr: { d: curve },
			ease: "power2.easeIn",
		}).to(svg, {
			duration: 0.5,
			attr: { d: flat },
			ease: "power2.easeOut",
		});
		tl.to(".preloader", {
			y: -1500,
		});
		tl.to(".preloader", {
			zIndex: -1,
			display: "none",
		});

		function startStrokeAnimation() {
			if (svgText) {
			  // Add a class or directly apply styles to trigger the stroke animation
			  svgText.classList.add("animate-stroke");
			}
		}


	});
      
    
})(jQuery);

/**
 *	ZYAN - Personal Portfolio Templete (HTML)
 *	Author: codeefly
 *	Author URL: http://themeforest.net/user/codeefly
 *	Copyright © ZYAN by codeefly. All Rights Reserved.
 **/

 (function ($) {
    "use strict";
    console.clear();
  
    var isMobile =
      /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Nokia|Opera Mini/i.test(
        navigator.userAgent
      )
        ? true
        : false;
  
      var zyan = {
      /* ZYAN init */
      init() {
        zyan.customMouse()
        zyan.magnificPopup()
      },
      /* Svg to image */
      imgToSvg() {
        document.querySelectorAll("img.svg").forEach((el) => {
          const imgID = el.getAttribute("id");
          const imgClass = el.getAttribute("class");
          const imgURL = el.getAttribute("src");
          fetch(imgURL)
            .then((data) => data.text())
            .then((response) => {
              const parser = new DOMParser();
              const xmlDoc = parser.parseFromString(response, "text/html");
              let svg = xmlDoc.querySelector("svg");
              if (typeof imgID !== "undefined") {
                svg.setAttribute("id", imgID);
              }
  
              if (typeof imgClass !== "undefined") {
                svg.setAttribute("class", imgClass + " replaced-svg");
              }
  
              svg.removeAttribute("xmlns:a");
              if (el.parentNode) {
                el.parentNode.replaceChild(svg, el);
              }
            });
        });
      },
      /** Mobile Menu */
      mobileMenu() {
        if ($(".main_menu").offset() != undefined) {
          var navoff = $(".main_menu").offset().top;
          $(window).scroll(function () {
            var scrolling = $(this).scrollTop();
  
            if (scrolling > navoff) {
              $(".main_menu").addClass("menu_fix");
            } else {
              $(".main_menu").removeClass("menu_fix");
            }
          });
        }
        /** Mobile Menu Button */
        $(".menu_2_icon").on("click", function () {
          $(".menu_2_icon").toggleClass("show_icon");
        });
        $(".menu_2_icon").on("click", function () {
          $(".main_menu_2").toggleClass("show_menu");
        });
        $(".navbar-toggler").on("click", function () {
          $(".navbar-toggler").toggleClass("show");
        });
      },
      /** counter */
      counter() {
        $(".counter").countUp();
      },
      /** Slick Slider */
      slickSlider() {
        $(".testi_slider").slick({
          slidesToShow: 2,
          slidesToScroll: 1,
          autoplay: true,
          autoplaySpeed: 2000,
          dots: false,
          arrows: false,
  
          responsive: [
            {
              breakpoint: 1200,
              settings: {
                slidesToShow: 2,
              },
            },
            {
              breakpoint: 992,
              settings: {
                slidesToShow: 1,
              },
            },
            {
              breakpoint: 768,
              settings: {
                slidesToShow: 1,
              },
            },
            {
              breakpoint: 576,
              settings: {
                slidesToShow: 1,
              },
            },
          ],
        });
      },
      /** marquee */
      marquee() {
        $(".marquee_animi").marquee({
          speed: 100,
          gap: 0,
          delayBeforeStart: 0,
          direction: "left",
          duplicated: true,
          pauseOnHover: true,
          startVisible: true,
        });
      },
      /** Sticky sidebar */
      stickySideBar() {
        $("#sticky_sidebar").stickit({
          top: 100,
        });
      },
      /** Animation */
      animation() {
        /** Fade Left */
        let fade_left = gsap.utils.toArray(".fade_left");
        gsap.set(fade_left, {
          opacity: 0,
          x: -30,
        });
  
        if (fade_left) {
          if (device_width < 1023) {
            fade_left.forEach((item, i) => {
              gsap.to(item, {
                scrollTrigger: {
                  trigger: item,
                  start: "top center+=150",
                  markers: false,
                },
                opacity: 1,
                x: 0,
                ease: "power2.out",
                duration: 2,
                stagger: {
                  each: 0.4,
                },
              });
            });
          } else {
            fade_left.forEach((item, i) => {
              const containerID = `#${item.getAttribute("data-trigerId")}`;
              gsap.to(
                `${containerID !== "#null" ? containerID : ""} .fade_left`,
                {
                  scrollTrigger: {
                    trigger: containerID !== "#null" ? containerID : ".fade_left",
                    start: "top center+=150",
                    markers: false,
                  },
                  opacity: 1,
                  x: 0,
                  ease: "power2.out",
                  duration: 2,
                  stagger: {
                    each: 0.4,
                  },
                }
              );
            });
          }
        }
  
        /** Fade Right */
        let fade_right = gsap.utils.toArray(".fade_right");
        gsap.set(fade_right, {
          opacity: 0,
          x: +30,
        });
  
        if (fade_right) {
          if (device_width < 1023) {
            fade_right.forEach((item, i) => {
              gsap.to(item, {
                scrollTrigger: {
                  trigger: item,
                  start: "top center+=150",
                  markers: false,
                },
                opacity: 1,
                x: 0,
                ease: "power2.out",
                duration: 2,
                stagger: {
                  each: 0.4,
                },
              });
            });
          } else {
            fade_right.forEach((item, i) => {
              const containerID = `#${item.getAttribute("data-trigerId")}`;
              const stagger = item.getAttribute("data-stagger");
              gsap.to(`${containerID} .fade_right`, {
                scrollTrigger: {
                  trigger: containerID,
                  start: "top center+=150",
                  markers: false,
                },
                opacity: 1,
                x: 0,
                ease: "power2.out",
                duration: 2,
                stagger: {
                  each: stagger ? stagger : 0.4,
                },
              });
            });
          }
        }
  
        /** Fade Bottom */
        let fade_bottom = gsap.utils.toArray(".fade_bottom");
        if (device_width < 1023) {
          fade_bottom.forEach((item, i) => {
            gsap.set(item, { opacity: 0, y: 60 });
            let featured2Timeline = gsap.timeline({
              scrollTrigger: {
                trigger: item,
                start: "top center+=200",
              },
            });
            featured2Timeline.to(item, {
              opacity: 1,
              y: 0,
              duration: 1.5,
              ease: "power4.out",
            });
          });
        } else {
          fade_bottom.forEach((item, i) => {
            const containerID = `#${item.getAttribute("data-trigerId")}`;
            const stagger = item.getAttribute("data-stagger");
            const duration = item.getAttribute("data-duration");
            const defaultValue = item.getAttribute("data-default-value");
            console.log(defaultValue);
            gsap.set(
              `${containerID !== "#null" ? containerID : ""} .fade_bottom`,
              {
                opacity: 0,
                y: defaultValue ? defaultValue : 30,
              }
            );
            gsap.to(
              `${containerID !== "#null" ? containerID : ""} .fade_bottom`,
              {
                scrollTrigger: {
                  trigger: containerID !== "#null" ? containerID : ".fade_bottom",
                  start: "top center+=200",
                },
                opacity: 1,
                y: 0,
                duration: duration ? duration : 2,
                ease: "power4.out",
                stagger: stagger ? stagger : 0.3,
              }
            );
          });
        }
      },
      /** Text animation */
      textAnimation() {
        if (device_width > 767) {
          var hasAnim = $(".text_hover_animaiton");
          if (hasAnim.length !== 0) {
            hasAnim.each(function () {
              var $this = $(this);
              var splitType = "words,chars";
              new SplitText($this, {
                type: splitType,
                wordsClass: "menu-text",
              });
            });
          }
        }
      },
      headingAnimation() {
        var hasAnim = $(".has-animation");
        if (device_width > 767) {
          hasAnim.each(function () {
            var $this = $(this);
            var splitType = "lines, chars";
            var splitto = new SplitText($this, {
              type: splitType,
              linesClass: "anim_line",
              charsClass: "anim_char",
              wordsClass: "anim_word",
            });
            var lines = $this.find(".anim_line"),
              words = $this.find(".anim_word"),
              chars = $this.find(".anim_char");
            gsap.fromTo(
              chars,
              { y: "100%" },
              {
                y: "0%",
                duration: 0.8,
                stagger: 0.01,
                ease: "power2.out",
                scrollTrigger: {
                  trigger: $(this).parent("div"),
                  start: "top center+=300",
                  toggleActions: "play none none none",
                },
              }
            );
          });
        }
      },
      progressbar() {
        var progressbar = $(".tf__team_skills_bar_single .fill");
        progressbar.each(function () {
          const percentage = progressbar.attr("data-percentage");
          gsap.fromTo(
            progressbar,
            { css: { width: 0 } },
            {
              scrollTrigger: {
                trigger: $(this).parent("div"),
                start: "top center+=300",
                toggleActions: "play none none none",
              },
              css: { width: `${percentage}%` },
              duration: 0.8,
              stagger: 0.01,
              ease: "power2.out",
            }
          );
        });
      },
      /** parallaxie */
      parallaxie() {
        $(".tf__subscribe").parallaxie({
          speed: 0.8,
          size: "cover",
        });
      },
      /** Preloader */
      preloader() {
        const svg = document.getElementById("svg");
        const tl = gsap.timeline();
        const curve = "M0 502S175 272 500 272s500 230 500 230V0H0Z";
        const flat = "M0 2S175 1 500 1s500 1 500 1V0H0Z";
  
        tl.to(".preloader-text", {
          delay: 0.5,
          y: -100,
          opacity: 0,
        });
        tl.to(svg, {
          duration: 0.1,
          // attr: { d: curve },
          ease: "power2.easeIn",
        }).to(svg, {
          duration: 0.5,
          attr: { d: flat },
          ease: "power2.easeOut",
        });
        tl.to(".preloader", {
          y: -1500,
        });
        tl.to(".preloader", {
          zIndex: -1,
          display: "none",
        });
      },
      /** Mouse */
      customMouse() {
        var mouse = { x: 0, y: 0 }; // Cursor position
        var pos = { x: 0, y: 0 }; // Cursor position
        var ratio = 0.15; // delay follow cursor
        var active = false;
        var ball = $("#ball");
  
        /** default */
        const defaultValue = {
          duration: 0.3,
          opacity: 0.5,
          width: "30px",
          height: "30px",
          backgroundColor: "transparent",
          border: "2px solid #fff",
        };
        const hoverBall = {
          duration: 0.3,
          css: {
            borderWidth: 0,
            opacity: "1!important",
            width: "95px!important",
            height: "95px!important",
            backgroundColor: "#fff",
          },
        };
        gsap.set(ball, {
          // scale from middle and style ball
          xPercent: -50,
          yPercent: -50,
        });
        document.addEventListener("mousemove", mouseMove);
        function mouseMove(e) {
          mouse.x = e.clientX;
          mouse.y = e.clientY;
        }
        gsap.ticker.add(updatePosition);
        function updatePosition() {
          if (!active) {
            pos.x += (mouse.x - pos.x) * ratio;
            pos.y += (mouse.y - pos.y) * ratio;
  
            gsap.set(ball, { x: pos.x, y: pos.y });
          }
        }
        // link
        $("a,.c-pointer,button,.progress")
          .not(".project_slider a") // omit from selection.
          .on("mouseenter", function () {
            gsap.to(ball, {
              duration: 0.3,
              borderWidth: 0,
              opacity: 0.5,
              backgroundColor: "#CCC",
              width: "80px",
              height: "80px",
            });
          })
          .on("mouseleave", function () {
            gsap.to(ball, defaultValue);
          });
        // Data cursor
        if ($("[data-cursor]")) {
          $("[data-cursor]").each(function () {
            $(this)
              .on("mouseenter", function () {
                ball.append('<div class="ball-view"></div>');
                $(".ball-view").append($(this).attr("data-cursor"));
                gsap.to(ball, hoverBall);
              })
              .on("mouseleave", function () {
                ball.find(".ball-view").remove();
                gsap.to(ball, defaultValue);
              });
          });
        }
        // Slider
        if ($(".slick-list")) {
          $(".slick-list").each(function () {
            $(this)
              .on("mouseenter", function () {
                ball.append(
                  '<div class="ball-drag"><i class="far fa-angle-left"></i><i class="far fa-angle-right"></i></div>'
                );
                // $(".ball-drag").append("read more");
                gsap.to(ball, hoverBall);
              })
              .on("mouseleave", function () {
                ball.find(".ball-drag").remove();
                gsap.to(ball, defaultValue);
              });
          });
        }
        // Gallery
        if ($(".gallery")) {
          $(".gallery").each(function () {
            $(this)
              .on("mouseenter", function () {
                ball.append(
                  '<div class="ball-gallery"><i class="fa-sharp fa-solid fa-eye"></i></div>'
                );
                // $(".ball-drag").append("read more");
                gsap.to(ball, hoverBall);
              })
              .on("mouseleave", function () {
                ball.find(".ball-gallery").remove();
                gsap.to(ball, defaultValue);
              });
          });
        }
      },
      magnificPopup() {
        $(".play_btn").each(function () {
          $(this).magnificPopup({
            type: "iframe",
            mainClass: "mfp-fade",
            preloader: false,
            fixedContentPos: true,
          });
        });
        $(".image_popup,.gallery_popup a").magnificPopup({
          type: "image",
          gallery: {
            enabled: true,
          },
          mainClass: "mfp-fade",
        });
        $(".details").magnificPopup({
          type: "inline",
          overflowY: "auto",
          closeBtnInside: true,
          mainClass: "mfp-fade zyan-popup",
        });
      },
      serviceHover() {
        const services = document.querySelectorAll(".tf__single_service_2");
        services.forEach((service) => {
          service.addEventListener("mouseenter", () => {
            document
              .querySelector(".tf__single_service_2.active")
              .classList.remove("active");
            service.classList.add("active");
          });
        });
      },
    };
    $(document).ready(function () {
      zyan.init();
      zyan.preloader();
    });
  })(jQuery);  