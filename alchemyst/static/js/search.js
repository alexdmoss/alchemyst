var lunrIndex,
    $results,
    documents;

function initLunr() {
    // retrieve the index file
    $.getJSON("/static/search.json")
        .done(function (index) {
            documents = index;

            lunrIndex = lunr(function () {

                this.ref("name");
                this.field('title', {
                    boost: 25
                });
                this.field('tags', {
                    boost: 20
                });
                this.field("description", {
                    boost: 15
                });
                this.field("category", {
                    boost: 5
                });
                this.field("level", {
                    boost: 5
                });

                documents.forEach(function (doc) {
                    try {
                        this.add(doc)
                    } catch (e) { }
                }, this)
            })
        })
        .fail(function (jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            console.error("Error getting Lunr index file:", err);
        });
}

function search(query) {
    return lunrIndex.search(query).map(function (result) {
        return documents.filter(function (page) {
            try {
                return page.name === result.ref;
            } catch (e) {
                console.error('Error in search results parsing', e);
            }
        })[0];
    });
}


/******************* Main Search Page *******************/

function initUI() {
    $results = $("#results");

    $("#search-menu").keyup(function () {

        // empty previous results
        $results.empty();

        // trigger search when at least two chars provided.
        var query = $(this).val();
        if (query.length < 2) {
            return;
        }

        var results = search(query);

        renderMenuResults(results);
    });
}

function renderMenuResults(results) {

    if (!results.length) {
        return;
    }

    $('#search-results').show();

    // results.slice(0, 10).forEach to limit to 10 results
    results.forEach(function (result) {
        var $result = $("<li class='search-result'>");

        // console.log(JSON.stringify(result))
        $result.append($("<a>", {
            href: "/note/" + result.name,
            alt: result.title,
            title: result.title,
            text: result.title
        }));

        $result.append($("<span>", {
            class: "search-result-description",
            text: " - " + result.description
        }));

        $results.append($result);

    });
}

/******************* Main Search Page *******************/

function searchForm() {
    $results = $("#results");

    $("#search-main").keyup(function () {

        // empty previous results
        $results.empty();

        // trigger search when at least two chars provided.
        var query = $(this).val();
        if (query.length < 2) {
            return;
        }

        var results = search(query);

        renderMainResults(results);
    });
}

function renderMainResults(results) {

    if (!results.length) {
        return;
    }

    $('#search-results').show();

    // results.slice(0, 10).forEach to limit to 10 results
    results.forEach(function (result) {
        var $result = $("<li class='search-result'>");

        // console.log(JSON.stringify(result))
        $result.append($("<a>", {
            href: "/note/" + result.name,
            alt: result.title,
            title: result.title,
            text: result.title
        }));

        $result.append($("<span>", {
            class: "search-result-description",
            text: " - " + result.description
        }));

        $results.append($result);

    });
}

/******************* Init *******************/

initLunr();

$(document).ready(function () {
    initUI();
    searchForm();
});