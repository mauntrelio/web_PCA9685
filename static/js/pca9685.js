var PCA9685 = (function($,window,document,undefined) {

  "use strict";

  var set_range_label = function(range) {
    range.next("div.range-value").find("span").html(range.val());
  };

  var update_pulse = function(index, start, end) {
    var freq = parseInt($("#freq").val());
    var length = Math.abs(start - end);
    var pulse_length = App.round(length / (4096 * freq ) * 1000, 2);
    $("#pulse_" + index).html(pulse_length + " ms");
  };

  var bind_ranges = function() {
    $("input[type=range].pwm").on("input",function(){
      var $this = $(this);
      var value = parseInt($this.val());
      var index = $this.data("index");
      set_range_label($this);
      var other = ($this.hasClass("start")) ? "end" : "start";
      var $other = $("#channel_"+index+"_"+other);
      if ($other.length) {
        var other_value = parseInt($other.val());
        var test = (other_value <= value);
        var new_value = value + 1;
        if (other == "start") {
          test = (other_value > value);
          new_value = value - 1;
        }
        if (test) {
          $other.val(new_value);
        }
        set_range_label($other);
      }
      $("#pwm_"+index).addClass("danger");
      update_pulse(index, value, other_value);
    });

    $("#freq").on("input",function(){
      var $this = $(this);
      var value = parseInt($this.val());
      var old_value = $this.data("orig-value");
      set_range_label($this);
      if (value != old_value) {
        $this.parent("div").addClass("bg-danger");
      } else {
        $this.parent("div").removeClass("bg-danger");
      }
    });

    $("#freq").on("change",function(){
      var $this = $(this);
      var value = parseInt($this.val());
      $("input[type=range].pwm.start").each(function(){
        var $this = $(this);
        var index = $this.data("index");
        var start_value = parseInt($this.val());
        var end_value = parseInt($("#channel_"+index+"_end").val());
        update_pulse(index, start_value, end_value);
      });
    });
  }

  var bind_buttons = function () {
    $("#set_freq").on("click",function(){
      var $freq = $("#freq");
      $.post("/set", { "freq": $freq.val() }, function(data){
        console.log(data);
        $freq.data("orig-value", data.freq);
        $freq.attr("data-orig-value", data.freq);
        $freq.parent("div").removeClass("bg-danger");
        $freq.parent("div").flash();
      });
    });

    $(".set_pwm").on("click",function(){
      var $this = $(this);
      var index = $this.data("index");
      var channel_start = "channel_" + index + "_start";
      var channel_end = "channel_" + index + "_end";
      var $channel_start = $("#"+channel_start);
      var $channel_end = $("#"+channel_end);
      var start = $channel_start.val();
      var end = $channel_end.val();
      var post_data = {};
      post_data[channel_start] = start;
      post_data[channel_end] = end;
      $.post("/set", post_data,
        function(data){
          var start = data.channels[index].start;
          var end = data.channels[index].end;
          console.log(data);
          $channel_start.data("orig-value", start).attr("data-orig-value", start);
          $channel_end.data("orig-value", end).attr("data-orig-value", end);
          $("#pwm_"+index).removeClass("danger").flash();
      });
    });

    $(".undo_pwm").on("click",function(){
      var $this = $(this);
      var index = $this.data("index");
      var $start = $("#channel_" + index + "_start");
      var $end = $("#channel_" + index + "_end");
      var start_value = $start.data("orig-value");
      var end_value = $end.data("orig-value");
      $start.val(start_value).trigger("input");
      $end.val(end_value).trigger("input");
      $("#pwm_"+index).removeClass("danger");
    });

    $("#set_all").on("click",function(){
      $(".set_pwm").trigger("click");
    });

    $("#reset_all").on("click",function(){
      var post_data = {};
      var channel_start, channel_end;

      for (var i = 0; i < 16; i++) {
        var channel_start = "channel_" + i + "_start";
        var channel_end = "channel_" + i + "_end";
        $("#" + channel_start).val(0);
        $("#" + channel_end).val(0);
        $("#pwm_"+i).addClass("danger");
        post_data[channel_start] = 0;
        post_data[channel_end] = 0;
      }

      $.post("/set", post_data, function() { window.location.reload(); });

    });

  };

  var init = function() {
    bind_ranges();
    bind_buttons();
  };

  return {
    init: init
  };

}(jQuery, window, document));
