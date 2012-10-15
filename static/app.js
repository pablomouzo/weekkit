require.config({
  baseUrl: '/static',
  paths: {
    subreddit: 'app/subreddit',
    search: 'app/search'
  },
  'shim': 
  {
    underscore: {
      'exports': '_'
    },
    backbone: {
      'deps': ['jquery', 'underscore'],
      'exports': 'Backbone'
    }
  }   
}); 

require(
  ["require", "jquery", "underscore", "backbone",
   "subreddit", "search",
   "django-ajax-post", "/static/bootstrap/js/bootstrap.min.js"],
  function(require, $, _, Backbone, Subreddit, search) {
    $(function() {
      /* Application events aggregator */
      var vent = _.extend({}, Backbone.Events);

      var searchResults = new search.SearchResults();

      var searchResultsListView = new search.SearchResultsListView({
        results: searchResults
      });

      var MySubredditsView = Backbone.View.extend({

        el: $("#my-subreddits"),
        template: _.template($("#my-subreddits-item-template").html()),

        initialize: function(options){
          Backbone.View.prototype.initialize.call(this, options);
          vent.on("subreddit:added", this.add, this);
        },

        add: function(subreddit){
          this.$el.append(
            this.template(subreddit.toJSON())
          );
        }
      });

      var mySubredditsView = new MySubredditsView();

      // Search bar handler
      var searchBuffer = {
        SEARCH: false,
        QUERY: "",

        search: function() {
          if (!this.SEARCH) { return; }
          this.SEARCH = false;
          var url = "/search_subreddit_names/?query=" + this.QUERY;
          $.getJSON(url, function(data) {
            searchResults.reset(data);
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
    
  }
);
