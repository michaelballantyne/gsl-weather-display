// The standard Ico Normalizer didn't use much of the vertical space available to it with the sort
// of data we are graphing, so we modify it. Because we do these modifications, we use the non-minified
// version of Ico.
Ico.Normaliser.prototype = {
    calculateStart: function() {
        var min = typeof this.options.start_value !== 'undefined' && this.min >= 0 ? this.options.start_value : this.min,
        // we'll have the graph start one step below our data
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

    process: function() {
        this.range = this.max - this.start_value;
        this.step = this.labelStep(this.range);
    },

    labelStep: function(value) {
        return 0.2
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

// Apply layout.
var size = function() {
    var screenh = $(window).height();
    var screenw = $(window).width();

    // We'll use a two column layout if the horizontal screen resoultion is >= 1000.
    var twocol = screenw >= 1000;

    // Apply or remove classes that create the two column layout.
    if (twocol) {
        $('*').addClass('twocol');
    } else {
        $('*').removeClass('twocol');
    }

    var graph = $('#graph');
    var graphbox = $('#levelbox');

    var gaddh = screenh - (graphbox.offset().top + graphbox.outerHeight())

    // If in the two column layout, ideally we'd like the graph to end nearly at the
    // bottom of the screen, with just some padding. In the one column layout, we
    // want to be sure the use knows there is more to the page to scroll to.
    if (twocol) {
        var leftover = 20;
    } else {
        var leftover = 80;
    }

    var gnewh = graph.height() + gaddh - leftover;

    // If the screen hight is small enough, the graph could be too small. Make sure it
    // is at least 300px high, even if that means the user must scroll.
    var minGraphHeight = 300;
    if (gnewh < minGraphHeight) {
        gnewh = minGraphHeight;
    }

    graph.height(gnewh);

    var radarbox = $('#radarbox')
    var radarimg = $('#radarbox img')
    
    radarbox.css('marginTop', 0);

    // In two column layout, push radar image down so that the bottom of it 
    // matches with the bottom of the graph
    if (twocol) {
        var bottom = screenh - leftover;
        var raddh = bottom - (radarbox.offset().top + radarbox.outerHeight())

        if (raddh > 0) {
            radarbox.css('marginTop', raddh);
        }
    }
}


var createGraph = function() {
    // Remove graph if we've drawn it before.
    $('#graph').html('');

    new Ico.LineGraph($('#graph')[0], {saline: lakedata.saline, saltair: lakedata.saltair}, {
        stroke_width: "1",
        width: $('#graph').width(),
        height: $('#graph').height(),
        curve_amount: 0,
        // Ico should figure this out from the div it is inside, but that is broken on IE
        background_colour: "#FFFFFF",
        labels: lakedata.labels,
        colours: {
            saline: "#AD1F00", // north, red
            saltair: "#2a9338" // south, green
        }
    });

    // The graph was oddly positioned in IE8 without this.
    $('#graph div').css('overflow', 'visible')
}

// Show an error if when the page is loaded, the data provided is more than 15 minutes out of date.
var checkdate = function() {
    // getTime provides milliseconds from UTC epoch. Our generated time is in seconds since the epoch, so divide by 1000.
    var current = (new Date()).getTime() / 1000;
    var difference = current - generated;
    if (difference > 900) {
        if ($('#error').length == 0) {
            $('#contentFrame').prepend('<div id="error">' + errormsg + '</div>');
        }
    }
}

// We need the radar image to be loaded so that its dimensions are known
// to the layout engine before we try and lay the page out, so wait
// till onLoad rather than use jQuery's DOM ready.
$(window).load(function() {
    checkdate();

    size();

    // The content starts out hidden so that the user doesn't see it draw
    // and then be moved. Must set visible before we draw graph or it won't appear in IE8.
    $('#contentArea').css('visibility', 'visible');
    
    createGraph();

    // Resize elements and redraw after window resize, but only after they've stopped dragging.
    $(window).resize(debounce(500, function() {
        size();
        createGraph();
    }));
});
