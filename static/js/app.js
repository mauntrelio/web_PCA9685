var App = (function($,window,document,undefined){

  "use strict";

  var App = {};

  App.init = function(){

    // init GUI interaction
    if (typeof PCA9685 !== "undefined") {
      PCA9685.init();
    }

    // add a flash() method to jQuery
    $.fn.flash =  function() {
      var $this = this;
      $this.addClass("flash");
      setTimeout( function(){
        $this.removeClass("flash");
      }, 1000);
    }

  };

  // add a round method with number of decimals
  App.round = function(number, precision) {
    var factor = Math.pow(10, precision);
    var tempNumber = number * factor;
    var roundedTempNumber = Math.round(tempNumber);
    return roundedTempNumber / factor;
  };

  return App;

}(jQuery,window,document));


$(function(){
  App.init();
})
