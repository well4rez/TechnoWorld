// Utilities for parsing and formatting prices with space thousands separator
(function(window){
    function parsePriceString(s){
        if (s === null || s === undefined) return 0;
        s = String(s).replace(/\s/g, '').replace('₽', '').trim().replace(',', '.');
        var n = parseFloat(s);
        return isNaN(n) ? 0 : n;
    }

    function formatNumberWithSpaces(num){
        if (num === null || num === undefined) return '';
        var n = Number(num);
        if (isNaN(n)) return '';
        var isInt = Number.isInteger(n);
        var parts = isInt ? [String(Math.round(n)), ''] : n.toFixed(2).split('.');
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
        // Remove trailing zeros in decimal part
        if (parts[1]) {
            parts[1] = parts[1].replace(/0+$/, '');
            return parts[1] ? parts[0] + '.' + parts[1] : parts[0];
        }
        return parts[0];
    }

    window.priceUtils = {
        parsePriceString: parsePriceString,
        formatNumberWithSpaces: formatNumberWithSpaces
    };
})(window);
