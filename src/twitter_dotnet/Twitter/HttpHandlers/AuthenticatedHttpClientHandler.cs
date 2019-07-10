using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using JetBrains.Annotations;

namespace Twitter.HttpHandlers
{
    /// <summary>
    /// A custom <see cref="HttpClientHandler"/> to handle search requests
    /// </summary>
    internal sealed class AuthenticatedHttpClientHandler : HttpClientHandler
    {
        [NotNull]
        private readonly string AppName;

        [NotNull]
        private readonly string AccessToken;

        public AuthenticatedHttpClientHandler([NotNull] string appName, [NotNull] string accessToken)
        {
            AppName = appName;
            AccessToken = accessToken;
        }

        /// <inheritdoc/>
        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            // Headers setup
            request.Headers.Add("User-Agent", AppName);
            request.Headers.Add("Authorization", $"Bearer {AccessToken}");

            // Send the request
            return base.SendAsync(request, cancellationToken);
        }
    }
}

