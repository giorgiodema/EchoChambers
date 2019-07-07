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
    }
}
