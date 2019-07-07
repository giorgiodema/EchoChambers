using Newtonsoft.Json;

namespace Twitter.Models
{
    /// <summary>
    /// A model that represents a Twitter user
    /// </summary>
    public sealed class User
    {
        /// <summary>
        /// Gets the id of the user
        /// </summary>
        [JsonProperty("id")]
        public ulong Id { get; internal set; }

        /// <summary>
        /// Gets the screen name of the user
        /// </summary>
        [JsonProperty("screen_name")]
        public string ScreenName { get; internal set; }

        /// <summary>
        /// Gets the description of the user
        /// </summary>
        [JsonProperty("description")]
        public string Description { get; internal set; }
    }
}
