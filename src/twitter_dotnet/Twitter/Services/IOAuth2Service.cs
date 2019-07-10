using System.Threading.Tasks;
using Refit;

namespace Twitter.Services
{
    public interface IOAuth2Service
    {
        [Post("/oauth2/token")]
        Task<string> AuthenticateAsync([Body(BodySerializationMethod.UrlEncoded)] string body = "grant_type=client_credentials");
    }
}
