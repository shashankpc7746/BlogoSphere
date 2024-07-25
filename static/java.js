window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("scrollBtn").style.display = "block";
  } else {
    document.getElementById("scrollBtn").style.display = "none";
  }
}

function scrollToTop() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

document.addEventListener("DOMContentLoaded", () => {
  const themeToggleInput = document.getElementById("themeToggleCheckbox");
  const body = document.body;

  // Function to toggle theme based on checkbox state
  const toggleTheme = () => {
    if (themeToggleInput.checked) {
      // Dark theme
      body.classList.add("dark-theme");
      // Save theme preference to localStorage
      localStorage.setItem("theme", "dark");
    } else {
      // Light theme
      body.classList.remove("dark-theme");
      // Remove theme preference from localStorage
      localStorage.removeItem("theme");
    }
  };

  // Check for theme preference in localStorage
  const currentTheme = localStorage.getItem("theme");
  if (currentTheme === "dark") {
    // Set checkbox state and apply dark theme
    themeToggleInput.checked = true;
    body.classList.add("dark-theme");
  }

  // Add event listener to theme toggle input
  themeToggleInput.addEventListener("change", toggleTheme);
});

//<--------------Slider------------------->

// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Select all elements with the class 'wrapper'
  document.querySelectorAll(".wrapper").forEach((wrapper) => {
    // Find the '.card-wrapper' within the current 'wrapper'
    const cardWrapper = wrapper.querySelector(".card-wrapper");

    // Get the width of the first child element inside '.card-wrapper'
    const widthToScroll = cardWrapper.children[0].offsetWidth;

    // Find the previous and next arrow buttons within the current 'wrapper'
    const arrowPrev = wrapper.querySelector(".arrow.prev");
    const arrowNext = wrapper.querySelector(".arrow.next");

    // Initialize variables for the current scroll position, initial mouse position, and dragging state
    let currScroll = 0;
    let initPos = 0;
    let clicked = false;

    // Disable dragging on images and links within the 'wrapper'
    wrapper.querySelectorAll("img, a").forEach((item) => {
      item.setAttribute("draggable", false);
    });

    // Set up the click event for the previous arrow button
    arrowPrev.onclick = function () {
      // Scroll left by the width of one item
      cardWrapper.scrollLeft -= widthToScroll;
    };

    // Set up the click event for the next arrow button
    arrowNext.onclick = function () {
      // Scroll right by the width of one item
      cardWrapper.scrollLeft += widthToScroll;
    };

    // Handle mouse down event on the '.card-wrapper'
    cardWrapper.onmousedown = function (e) {
      // Add the 'grab' class to change the cursor to grabbing
      cardWrapper.classList.add("grab");

      // Record the initial mouse X position
      initPos = e.clientX;

      // Save the current scroll position
      currScroll = cardWrapper.scrollLeft;

      // Set the dragging state to true
      clicked = true;
    };

    // Handle mouse move event on the '.card-wrapper'
    cardWrapper.onmousemove = function (e) {
      // Only proceed if the mouse is currently down (dragging)
      if (clicked) {
        // Calculate the new X position
        const xPos = e.clientX;

        // Update the scroll position based on the mouse movement
        cardWrapper.scrollLeft = currScroll - (xPos - initPos);
      }
    };

    // Handle mouse up and mouse leave events on the '.card-wrapper'
    cardWrapper.onmouseup = mouseUpandLeave;
    cardWrapper.onmouseleave = mouseUpandLeave;

    // Function to reset dragging state
    function mouseUpandLeave() {
      // Remove the 'grab' class to revert the cursor
      cardWrapper.classList.remove("grab");

      // Set the dragging state to false
      clicked = false;
    }
  });
});
