using Newtonsoft.Json;

namespace Twitter.Models.Bundled
{
    /// <summary>
    /// A model that represents a parsed URL in a tweet
    /// </summary>
    public sealed class Url
    {
        /// <summary>
        /// Gets the raw URL used by the author of the tweet
        /// </summary>
        [JsonProperty("url")]
        public string RawUrl { get; internal set; }

        /// <summary>
        /// Gets the fully expanded URL for the current instance
        /// </summary>
        [JsonProperty("expanded_url")]
        public string ExpandedUrl { get; internal set; }
    }
}
