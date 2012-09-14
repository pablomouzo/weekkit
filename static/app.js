$(function() {

  /* Application events aggregator */
  var vent = _.extend({}, Backbone.Events);


  /* Simple model to represent a subreddit
     name: subreddit name
  */
  var Subreddit = Backbone.Model.extend({
    defaults: {
      name: "",
      description: ""
    },

    /* Get the subreddit description */
    getDescription: function() {
      var that = this;
      var url = "/reddit_proxy/r/" + this.get("name") + "/about.json";
      $.getJSON(url, function(response) {
        that.set("description", response.data.title);
      });
    },

    /* Add subreddit to the user subreddits list */
    addSubreddit: function() {
      var that = this;
      var tpl = _.template($("#my-subreddits-item-template").html());
      $.post(
        "/add_subreddit/",
        {name: that.get("name")},
        function(response) {
          vent.trigger("subreddit:added", that);
        }
      );
    }
  });

  /* Collection to store the results of a search
     This will be reseted on each search
  */
  var SearchResults = Backbone.Collection.extend({
    model: Subreddit
  });

  var searchResults = new SearchResults();

  /* Single result view */
  var SearchResultView = Backbone.View.extend({
    template: _.template($("#search-result-template").html()),

    events: {
      "click .subreddit-get-description": "getDescription",
      "click .subreddit-add": "addSubreddit"
    },

    initialize: function(options) {
      Backbone.View.prototype.initialize.call(this, options);
      this.model.on("change", this.render, this);
    },
    
    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },
    
    getDescription: function() {
      this.$(".subreddit-description").html("Loading...");
      this.model.getDescription();
    },

    addSubreddit: function() {
      this.model.addSubreddit();
    }
  });
  

  /* Results list view
     Will render each time we have new results
  */
  var SearchResultsListView = Backbone.View.extend({
    el: $("#search-results"),

    initialize: function(options){
      Backbone.View.prototype.initialize.call(this, options);
      this.results = options.results;
      this.results.on("reset", this.render, this);
    },
    
    render: function(){
      var that = this;
      this.$el.html("");
      this.results.each(function(result){
        var resultView = new SearchResultView({model: result});
        that.$el.append(resultView.render().el);
      });
      return this;
    }
  });

  var searchResultsListView = new SearchResultsListView({results: searchResults});

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
      var url = "/reddit_proxy/api/subreddits_by_topic.json?query=" + this.QUERY;
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
