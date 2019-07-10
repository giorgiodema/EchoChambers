using System;
using System.Diagnostics.CodeAnalysis;
using Newtonsoft.Json;
using Twitter.Models.Base;

namespace Twitter.Models
{
    /// <summary>
    /// A model that represents a single tweet
    /// </summary>
    public sealed class Tweet : IEquatable<Tweet>
    {
        /// <summary>
        /// Gets the id for the current tweet
        /// </summary>
        [JsonProperty("id")]
        public ulong Id { get; internal set; }

        /// <summary>
        /// Gets the text of the current tweet
        /// </summary>
        [JsonProperty("text")]
        public string Text { get; internal set; }

        /// <summary>
        /// Gets the author of the current tweet
        /// </summary>
        [JsonProperty("user")]
        public User User { get; internal set; }

        /// <summary>
        /// Gets the additional metadata for the current tweet
        /// </summary>
        [JsonProperty("entities")]
        public Entities Entities { get; internal set; }

        /// <summary>
        /// Gets the retweeted tweet, if present
        /// </summary>
        [JsonProperty("retweeted_status")]
        public Tweet Retweet { get; internal set; }

        /// <summary>
        /// Gets the creation time for the current tweet
        /// </summary>
        [JsonProperty("created_at")]
        public string CreationTime { get; internal set; }

        /// <inheritdoc/>
        public bool Equals(Tweet other) => other?.Id == Id;

        /// <inheritdoc/>
        public override bool Equals(object obj) => obj is Tweet tweet && tweet.Equals(this);

        /// <inheritdoc/>
        [SuppressMessage("ReSharper", "NonReadonlyMemberInGetHashCode")]
        public override int GetHashCode() => Id.GetHashCode();
    }
}
