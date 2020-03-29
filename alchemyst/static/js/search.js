var lunrIndex,
    $resultsMain,
    $resultsMenu,
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
    $resultsMenu = $("#results-popup");

    $("#search-menu").keyup(function () {

        // empty previous results
        $resultsMenu.empty();

        // trigger search when at least two chars provided.
        var query = $(this).val();
        if (query.length < 2) {
            return;
        }

        var resultsMenu = search(query);

        renderMenuResults(resultsMenu);
    });
}

function renderMenuResults(resultsMenu) {

    if (!resultsMenu.length) {
        return;
    }

    $('#search-popup').show();

    // resultsMenu.slice(0, 10).forEach to limit to 10 results
    resultsMenu.forEach(function (result) {
        var $result = $("<li class='popup-result'>");

        // console.log(JSON.stringify(result))
        $result.append($("<a>", {
            href: "/note/" + result.name,
            alt: result.title,
            title: result.title,
            text: result.title
        }));

        $result.append($("<br />"));
        $result.append($("<p>", {
            class: "popup-result-description",
            text: result.description
        }));
        // $result.append($("<hr />"));

        $resultsMenu.append($result);

    });

}

/******************* Main Search Page *******************/

function searchForm() {
    $resultsMain = $("#results-main");

    $("#search-main").keyup(function () {

        // empty previous results
        $resultsMain.empty();

        // trigger search when at least two chars provided.
        var query = $(this).val();
        if (query.length < 2) {
            return;
        }

        var resultsMain = search(query);

        renderMainResults(resultsMain);
    });
}

function renderMainResults(resultsMain) {

    if (!resultsMain.length) {
        return;
    }

    $('#search-results').show();

    // results.slice(0, 10).forEach to limit to 10 results
    resultsMain.forEach(function (result) {
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

        $resultsMain.append($result);

    });
}

/******************* Init *******************/

initLunr();

$(document).ready(function () {
    initUI();
    searchForm();
});