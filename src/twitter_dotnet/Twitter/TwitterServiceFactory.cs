using System;
using System.Net;
using System.Net.Http;
using System.Text;
using JetBrains.Annotations;
using Refit;
using Twitter.HttpHandlers;
using Twitter.Services;

namespace Twitter
{
    public static class TwitterServiceFactory
    {
        public const string BaseUrl = "https://api.twitter.com/";

        /// <summary>
        /// Gets a new <see cref="IOAuth2Service"/> instance
        /// </summary>
        /// <param name="appName">The name of the current application</param>
        /// <param name="clientId">The client id for the current application</param>
        /// <param name="secretId">The secret id for the current application</param>
        [Pure, NotNull]
        public static IOAuth2Service GetOAuth2Service([NotNull] string appName, [NotNull] string clientId, [NotNull] string secretId)
        {
            // URL encoding
            string
                urlClientId = WebUtility.UrlEncode(clientId),
                urlSecretId = WebUtility.UrlEncode(secretId),
                concat = $"{urlClientId}:{urlSecretId}";

            // Get the base64 string
            byte[] concatBytes = Encoding.UTF8.GetBytes(concat);
            string base64 = Convert.ToBase64String(concatBytes);

            HttpClient client = new HttpClient(new AuthenticatingHttpClientHandler(appName, base64))
            {
                BaseAddress = new Uri(BaseUrl)
            };
            return RestService.For<IOAuth2Service>(client);
        }

        /// <summary>
        /// Gets an <see cref="ITweetsService"/> instance to retrieve tweets and other objects
        /// </summary>
        /// <param name="appName">The name of the current application</param>
        /// <param name="accessToken">The access token to use to execute the API calls</param>
        [Pure, NotNull]
        public static ITweetsService GetTweetsService([NotNull] string appName, [NotNull] string accessToken)
        {
            HttpClient client = new HttpClient(new AuthenticatedHttpClientHandler(appName, accessToken))
            {
                BaseAddress = new Uri(BaseUrl)
            };
            return RestService.For<ITweetsService>(client);
        }
    }
}
