const cardSelector = '.project-card';
const searchSelector = 'input#projects-search'
const noResultsSelector = '#no-results'
let currentFilters = new Set();
let sortOrder = 'updated'
let searchTerm = ''

const getUpdateDate = e => $(e).find('#card-updated')[0].attributes['data-card-updated'].value;
const getTitle = e => $(e).find('h2').text();

const checkNoResults = () => {
    if ($(cardSelector + ':visible').length === 0) {
        $(noResultsSelector).show();
    } else {
        $(noResultsSelector).hide();
    };
}

const processText = (text) => {
    let processedText = text.toLowerCase();
    return processedText
}

const toggleFiltersVis = () => {
    $('.filters-container').toggleClass('closed');
    $('.filters-toggle').toggleClass('toggle');
}

const cardSort = (e) => {
    if (sortOrder !== e.value) {
        sortOrder = e.value;
        const cardsSort = $(cardSelector);
        const sortList = Array.prototype.sort.bind(cardsSort);

        switch (sortOrder) {
            case 'updated':
                sortList((a, b) => {
                    const aDate = new Date(getUpdateDate(a));
                    const bDate = new Date(getUpdateDate(b));
                    if (aDate < bDate) {
                        return 1;
                    };
                    return -1;

                });
                $('#projects').append(cardsSort);
                break;
            default:
                sortList((a, b) => {
                    const aTitle = getTitle(a);
                    const bTitle = getTitle(b);
                    if (aTitle < bTitle) {
                        return -1;
                    };
                    return 1;
                });
                $('#projects').append(cardsSort);

                break;
        }
    }
}

const singleFilterToggle = (filter, e) => {
    // visually toggle filter markup
    $(e).toggleClass('selected');
    // keep track of filters
    currentFilters.has(filter) ? currentFilters.delete(filter) : currentFilters.add(filter);
    // trigger filtering
    filterCards();
};

const filterCards = () => {
    if (currentFilters.size === 0) {
        // if no filters selected show all cards
        $(cardSelector).removeClass('filter-hide');
    } else {
        // hide all for animation
        $(cardSelector).addClass('filter-hide');
        $(cardSelector).each(function () {
            // get tags from individual card markup
            const itemTags = $(this)[0].attributes['data-tags'].value.split(', ');
            let show = false;
            // compare tags to tracked filters.
            // if filter is present, mark that this card should be shown.
            itemTags.map(tag => {
                if (currentFilters.has(tag)) { show = true; }
            });
            show ? $(this).removeClass('filter-hide') : $(this).addClass('filter-hide');
        })
        checkNoResults();
    }
}

const searchCards = (e) => {
    if (e) e.preventDefault();
    const term = document.getElementById('projects-search').value.toLowerCase();
    if (term === '') {
        $(cardSelector).removeClass('search-hide');
        checkNoResults();
    } else {
        $(cardSelector).addClass('search-hide');
        $(cardSelector).each(function () {
            let show = false;
            if ($(this)[0].outerText.toLowerCase().indexOf(processText(term)) !== -1) { show = true; }
            show ? $(this).removeClass('search-hide') : $(this).addClass('search-hide');
        })
        checkNoResults();
    }
    return false;
}
