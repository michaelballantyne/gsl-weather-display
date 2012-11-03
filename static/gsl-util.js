
Ico.Normalizer = Ico.Normaliser = function(data, options) {
    this.options = {
        start_value: null
    };

    if (typeof options !== 'undefined') {
        this.options = options;
    }

    this.min = Helpers.min(data);
    this.max = this.options.max || Helpers.max(data);
    this.standard_deviation = Helpers.standard_deviation(data);
    this.range = 0;
    this.step = this.labelStep(this.max - this.min);
    this.start_value = this.calculateStart();
    this.process();
};

Ico.Normaliser.prototype = {
    /**
     * Calculates the start value.  This is often 0.
     * @returns {Float} The start value 
     */
    calculateStart: function() {
        var min = typeof this.options.start_value !== 'undefined' && this.min >= 0 ? this.options.start_value : this.min,
        start_value = min - this.step;

        /* This is a boundary condition */
        if (this.min > 0 && start_value > this.min) {
            return 0;
        }

        if (this.min === this.max) {
            return 0;
        }

        return start_value;
    },

    /* Given a value, this method rounds it to the nearest good value for an origin */
    round: function(value, offset) {
        offset = offset || 1;
        var roundedValue = value;

        if (this.standard_deviation > 0.1) {
            var multiplier = Math.pow(10, -offset);
            roundedValue = Math.round(value * multiplier) / multiplier;

            if (roundedValue > this.min) {
                return this.round(value - this.step);
            }
        }
        return roundedValue;
    },

    /**
     * Calculates the range and step values.
     */
    process: function() {
        this.range = this.max - this.start_value;
        this.step = this.labelStep(this.range);
    },

    /**
     * Calculates the label step value.
     *
     * @param {Float} value A value to convert to a label position
     * @returns {Float} The rounded label step result
     */
    labelStep: function(value) {
        return value / 8;
    }
};


var b2width = $("#boxTwo").width();
var b2height = $("#boxTwo").height();
var b3width = $("#boxThree").width();
var b3height = $("#boxThree").height();

$("#boxTwoDims").html("" + b2width + " x " + b2height);
$("#boxThreeDims").html("" + b3width + " x " + b3height);

var a = new Ico.LineGraph($('#graph')[0], {saline: lakedata.saline, saltair: lakedata.saltair}, {
    width: 500, height: 300, stroke_width: "0", markers: "circle", marker_size: "2", labels: lakedata.labels});

