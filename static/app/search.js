define(["jquery", "underscore", "backbone", "subreddit"], function($, _, Backbone){

  var Subreddit = require('subreddit');

  /* Collection to store the results of a search
     This will be reseted on each search
  */
  var SearchResults = Backbone.Collection.extend({
    model: Subreddit
  });

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

  return {
    SearchResults: SearchResults,
    SearchResultView: SearchResultView,
    SearchResultsListView: SearchResultsListView
  };
  
});
