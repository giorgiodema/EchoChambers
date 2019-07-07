using System.IO;
using JetBrains.Annotations;
using Newtonsoft.Json;

namespace Twitter.Models.OAuth
{
    public sealed class OAuth2ClientInfo
    {
        [JsonProperty("application_name")]
        public string ApplicationName { get; internal set; }

        [JsonProperty("api_key")]
        public string ApiKey { get; internal set; }

        [JsonProperty("api_secret")]
        public string ApiSecret { get; internal set; }

        [JsonProperty("access_token")]
        public string AccessToken { get; internal set; }

        [Pure, NotNull]
        public static OAuth2ClientInfo LoadFromFile([NotNull] string path)
        {
            string json = File.ReadAllText(path);
            return JsonConvert.DeserializeObject<OAuth2ClientInfo>(json);
        }
    }
}
