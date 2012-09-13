$(function() {

  // Search results list view
  var searchResultsView = {
    $el: $("#search-results"),
    tpl: _.template($("#search-result-template").html()),
    render: function(results) {
      var that = this;
      this.$el.html("");
      _.each(results, function(result) {
        that.$el.append(that.tpl(result));
      });

      // Detail action
      $(".search-result button.subreddit-get-details").click(function(event) {
        var that = this;
        var $result = $(this).parents(".search-result");
        var $description = $result.children(".subreddit-description");
        if ($description.html() !== "") {
          return;
        }
        var id = $result.attr("id");
        var url = "/reddit_proxy/r/" + id + "/about.json";
        $description.html("Loading...");
        $description.show();
        $.getJSON(url, function(response) {
          console.log(response);
          $description.html(_.escape(response.data.title));
        });
      });

      // Add subreddit
      $(".search-result button.subreddit-add").click(function(event) {
        var that = this;
        var $result = $(this).parents(".search-result");
        var id = $result.attr("id");
        var tpl = _.template($("#my-subreddits-item-template").html());
        $.post(
          "/add_subreddit/",
          {name: id},
          function(response) {
            $(".my-subreddits").append(
              tpl({name: id})
            );
          }
        );
      });
    }
  };

  var searchBuffer = {
    SEARCH: false,
    QUERY: "",

    search: function() {
      if (!this.SEARCH) { return; }
      this.SEARCH = false;
      var url = "/reddit_proxy/api/subreddits_by_topic.json?query=" + this.QUERY;
      $.getJSON(url, function(data) {
        searchResultsView.render(data);
      });
    },

    query: function(q) {
      this.SEARCH = true;
      this.QUERY = q;
    }
  };

  setInterval(function() {
    searchBuffer.search();
  }, 1000);
  
  $("#subreddit-search").keyup(function() {
    var $input = $("#subreddit-search");
    searchBuffer.query($input.val());
  });
});
