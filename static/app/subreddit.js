define(
  ["require", "jquery", "underscore", "backbone"],
  function(require, $, _, Backbone){
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

    return Subreddit;
  }
);
