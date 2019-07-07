using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading;
using System.Threading.Tasks;
using JetBrains.Annotations;

namespace Twitter.HttpHandlers
{
    /// <summary>
    /// A custom <see cref="HttpClientHandler"/> to handle login requests
    /// </summary>
    internal sealed class AuthenticatingHttpClientHandler : HttpClientHandler
    {
        [NotNull]
        private readonly string AppName;

        [NotNull]
        private readonly string AccessToken;

        public AuthenticatingHttpClientHandler([NotNull] string appName, [NotNull] string base64token)
        {
            AppName = appName;
            AccessToken = base64token;
        }

        /// <inheritdoc/>
        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            // Headers setup
            request.Headers.Add("User-Agent", AppName);
            request.Headers.Add("Authorization", $"Basic {AccessToken}");
            request.Content.Headers.ContentType = new MediaTypeHeaderValue("application/x-www-form-urlencoded;charset=UTF-8");

            // Send the request
            return base.SendAsync(request, cancellationToken);
        }
    }
}
