
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


var debounce = function (threshold, func) {
    var timeout;
    return function debounced () {
        var obj = this, 
            args = arguments; 
        function delayed () {
            func.apply(obj, args); 
            timeout = null; 
        };
        if (timeout)
            clearTimeout(timeout);
        timeout = setTimeout(delayed, threshold || 100); 
    };
}

var size = function() {
    screenh = $(window).height();
    screenw = $(window).width();
    twocol = screenw >= 1000;

    graph = $('#graph');
    graphbox = $('#levelbox');

    gaddh = screenh - (graphbox.offset().top + graphbox.outerHeight())

    if (twocol) {
        leftover = 20;
    } else {
        leftover = 80;
    }

    gnewh = graph.height() + gaddh - leftover;

    minGraphHeight = 300;
    if (gnewh < minGraphHeight) {
        gnewh = minGraphHeight;
    }

    graph.height(gnewh);

    if (twocol) {
        setTimeout(function() {
        radarbox = $('#radarbox')
        radarimg = $('#radarbox img')
        
        radarbox.css('marginTop', 0);
        
        bottom = screenh - leftover;
        raddh = bottom - (radarbox.offset().top + radarbox.outerHeight())

        if (raddh > 0) {
            radarbox.css('marginTop', raddh);
        }
        }, 50);
    }
}


var createGraph = function() {
    $('#graph').html('');
    new Ico.LineGraph($('#graph')[0], {saline: lakedata.saline, saltair: lakedata.saltair}, {
        stroke_width: "1",
        curve_amount: 0,
        labels: lakedata.labels,
        colours: {
            saline: "#AD1F00",
            saltair: "#2a9338"
        }
    });
}

$(window).load(function() {
    size();
    createGraph();

    $(window).resize(debounce(250, function() {
        size();
        createGraph();
    }));
});
