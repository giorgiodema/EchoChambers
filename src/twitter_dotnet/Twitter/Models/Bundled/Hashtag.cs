using Newtonsoft.Json;

namespace Twitter.Models.Bundled
{
    /// <summary>
    /// A model that represents an hashtag in a tweet
    /// </summary>
    public sealed class Hashtag
    {
        /// <summary>
        /// Gets the text of the current hashtag
        /// </summary>
        [JsonProperty("text")]
        public string Text { get; internal set; }
    }
}
