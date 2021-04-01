function magnify(event){
  var mag = event.currentTarget;
  event.offsetX ? offsetX = event.offsetX : offsetX = event.touches[0].pageX
  event.offsetY ? offsetY = event.offsetY : offsetX = event.touches[0].pageX
  mag.style.backgroundPosition = (offsetX/mag.offsetWidth*100) + '% ' + (offsetY/mag.offsetHeight*100) + '%';
}

function clock(){
  // New release time
  var releaseDate = new Date("Mar 15, 2021 9:00:00").getTime();
  //timer - update every second
  var timer = setInterval(function() {
    // Get current time
    var current = new Date().getTime();
    // Get the difference
    var difference = releaseDate - current;
    if (difference > 0){
      // And calculate the days hours minutes and seconds from this
      var d = Math.floor(difference / (1000 * 60 * 60 * 24));
      var h = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var m = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
      var s = Math.ceil((difference % (1000 * 60)) / 1000);
      // Send back to the HTML
      document.getElementById("countdown").innerHTML = d + " days " + h + " hours " + m + " mins " + s + " secs ";
    }
  }, 1000);
}

clock()

// Recommended size slider section
// Appears on all items pages except beanies - not relevant for the product type
var slider = document.getElementById("weightslide");
var weight = document.getElementById("weightvalue");
var recsize = document.getElementById("recsize");
weight.innerHTML = slider.value;
recsize.innerHTML = 'Large (L)';

slider.oninput = function() {
  weight.innerHTML = this.value;
  if (this.value < 50) {
    recsize.innerHTML = "Extra Small (XS)";
  }
  else if (this.value >= 50 && this.value < 60) {
    recsize.innerHTML = "Small (S)";
  }
  else if (slider.value >= 60 && slider.value < 75) {
    recsize.innerHTML = "Medium (M)";
  }
  else if (slider.value >= 75 && slider.value < 90) {
    recsize.innerHTML = "Large (L)";
  }
  else if (slider.value >= 90 ) {
    recsize.innerHTML = "Extra Large (XL)";
  }
}
