(function () {
    "use strict";

    /**
     * Apply .scrolled class to the body as the page is scrolled down
     */
    function toggleScrolled() {
        const selectBody = document.querySelector("body");
        const selectHeader = document.querySelector("#header");
        if (!selectHeader) return;

        if (selectHeader.classList.contains("scroll-up-sticky") ||
            selectHeader.classList.contains("sticky-top") ||
            selectHeader.classList.contains("fixed-top")) {
            window.scrollY > 100 ? selectBody.classList.add("scrolled") : selectBody.classList.remove("scrolled");
        }
    }

    document.addEventListener("scroll", toggleScrolled);
    window.addEventListener("load", toggleScrolled);

    /**
     * Mobile nav toggle
     */
    const mobileNavToggleBtn = document.querySelector(".mobile-nav-toggle");

    if (mobileNavToggleBtn) {
        mobileNavToggleBtn.addEventListener("click", function () {
            document.body.classList.toggle("mobile-nav-active");
            this.classList.toggle("bi-list");
            this.classList.toggle("bi-x");
        });
    }

    /**
     * Hide mobile nav on same-page/hash links
     */
    document.querySelectorAll("#navmenu a").forEach((navmenu) => {
        navmenu.addEventListener("click", () => {
            if (document.body.classList.contains("mobile-nav-active")) {
                document.body.classList.remove("mobile-nav-active");
                mobileNavToggleBtn?.classList.toggle("bi-list");
                mobileNavToggleBtn?.classList.toggle("bi-x");
            }
        });
    });

    /**
     * Toggle mobile nav dropdowns
     */
    document.querySelectorAll(".navmenu .toggle-dropdown").forEach((navmenu) => {
        navmenu.addEventListener("click", function (e) {
            e.preventDefault();
            this.parentNode.classList.toggle("active");
            const dropdown = this.parentNode.nextElementSibling;
            if (dropdown) dropdown.classList.toggle("dropdown-active");
            e.stopImmediatePropagation();
        });
    });

    /**
     * Preloader - Remove it once page loads
     */
    const preloader = document.querySelector("#preloader");
    if (preloader) {
        window.addEventListener("load", () => {
            preloader.style.display = "none";
        });
    }

    /**
     * Scroll to top button
     */
    let scrollTop = document.querySelector(".scroll-top");

    function toggleScrollTop() {
        if (scrollTop) {
            window.scrollY > 100 ? scrollTop.classList.add("active") : scrollTop.classList.remove("active");
        }
    }

    if (scrollTop) {
        scrollTop.addEventListener("click", (e) => {
            e.preventDefault();
            window.scrollTo({top: 0, behavior: "smooth"});
        });
    }

    window.addEventListener("load", toggleScrollTop);
    document.addEventListener("scroll", toggleScrollTop);

    /**
     * Animation on scroll function and init
     */
    function aosInit() {
        if (typeof AOS !== "undefined") {
            AOS.init({
                duration: 600,
                easing: "ease-in-out",
                once: true,
                mirror: false,
            });
        }
    }

    window.addEventListener("load", aosInit);

    /**
     * Auto generate the carousel indicators (Bootstrap 5+ Fix)
     */
    document.querySelectorAll(".carousel-indicators").forEach((carouselIndicator) => {
        const carousel = carouselIndicator.closest(".carousel");
        if (!carousel) return;

        carousel.querySelectorAll(".carousel-item").forEach((carouselItem, index) => {
            const isActive = index === 0 ? "active" : "";
            carouselIndicator.innerHTML += `<button type="button" data-bs-target="#${carousel.id}" data-bs-slide-to="${index}" class="${isActive}" aria-label="Slide ${index + 1}"></button>`;
        });
    });

    /**
     * Initiate GLightbox
     */
    if (typeof GLightbox !== "undefined") {
        GLightbox({selector: ".glightbox"});
    }

    /**
     * Init isotope layout and filters
     */
    document.querySelectorAll(".isotope-layout").forEach(function (isotopeItem) {
        let layout = isotopeItem.getAttribute("data-layout") || "masonry";
        let filter = isotopeItem.getAttribute("data-default-filter") || "*";
        let sort = isotopeItem.getAttribute("data-sort") || "original-order";

        let initIsotope;
        if (typeof imagesLoaded !== "undefined") {
            imagesLoaded(isotopeItem.querySelector(".isotope-container"), function () {
                initIsotope = new Isotope(isotopeItem.querySelector(".isotope-container"), {
                    itemSelector: ".isotope-item",
                    layoutMode: layout,
                    filter: filter,
                    sortBy: sort,
                });
            });
        }

        isotopeItem.querySelectorAll(".isotope-filters li").forEach(function (filterBtn) {
            filterBtn.addEventListener("click", function () {
                let activeFilter = isotopeItem.querySelector(".isotope-filters .filter-active");
                if (activeFilter) activeFilter.classList.remove("filter-active");
                this.classList.add("filter-active");

                if (initIsotope) {
                    initIsotope.arrange({filter: this.getAttribute("data-filter")});
                    if (typeof aosInit === "function") aosInit();
                }
            });
        });
    });

    /**
     * Animate the skills items on reveal
     */
    document.querySelectorAll(".skills-animation").forEach((item) => {
        new Waypoint({
            element: item,
            offset: "80%",
            handler: function () {
                item.querySelectorAll(".progress .progress-bar").forEach((el) => {
                    el.style.width = el.getAttribute("aria-valuenow") + "%";
                });
            },
        });
    });

    /**
     * Init Swiper sliders
     */
    function initSwiper() {
        document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
            let configElement = swiperElement.querySelector(".swiper-config");
            if (!configElement) return;

            let config = JSON.parse(configElement.innerHTML.trim());
            new Swiper(swiperElement, config);
        });
    }

    window.addEventListener("load", initSwiper);
})();


var swiper = new Swiper('.swiper-container', {
    loop: true,
    autoplay: {delay: 3000},
    pagination: {el: '.swiper-pagination', clickable: true},
    navigation: {nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev'}
});


<!-- JavaScript to Open Modal -->
function openModal(videoId) {
    let videoFrame = document.getElementById("videoFrame");
    videoFrame.src = "https://www.youtube.com/embed/" + videoId;
    let modal = new bootstrap.Modal(document.getElementById("videoModal"));
    modal.show();
}