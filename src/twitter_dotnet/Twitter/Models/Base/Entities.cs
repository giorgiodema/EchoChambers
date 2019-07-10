using System.Collections.Generic;
using Newtonsoft.Json;
using Twitter.Models.Bundled;

namespace Twitter.Models.Base
{
    /// <summary>
    /// A model that represents a collection of attributes and info for a given tweet
    /// </summary>
    public sealed class Entities
    {
        /// <summary>
        /// Gets the collection of hashtags in a given tweet
        /// </summary>
        [JsonProperty("hashtags")]
        public IList<Hashtag> Hashtags { get; internal set; }

        /// <summary>
        /// Gets the collection of URLs in a given tweet
        /// </summary>
        [JsonProperty("urls")]
        public IList<Url> Urls { get; internal set; }
    }
}
