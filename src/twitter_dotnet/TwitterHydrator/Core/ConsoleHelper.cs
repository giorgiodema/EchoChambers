using System;
using JetBrains.Annotations;
using TwitterHydrator.Enums;

namespace TwitterHydrator.Core
{
    /// <summary>
    /// A small <see langword="class"/> with some helper methods to print info to the user
    /// </summary>
    internal static class ConsoleHelper
    {
        /// <summary>
        /// Shows a message to the user
        /// </summary>
        /// <param name="type">The type of message being displayed</param>
        /// <param name="message">The text of the message</param>
        public static void Write(MessageType type, [NotNull] string message)
        {
            switch (type)
            {
                case MessageType.Default:
                    Console.ForegroundColor = ConsoleColor.White;
                    Console.WriteLine(message);
                    break;
                case MessageType.Error:
                    WriteTaggedMessage(ConsoleColor.DarkYellow, "[ERROR]", message);
                    break;
                case MessageType.Info:
                    WriteTaggedMessage(ConsoleColor.DarkCyan, ">>", message);
                    break;
                default: throw new ArgumentOutOfRangeException(nameof(type), "Invalid message type");
            }
        }

        // Shows a tagged message to the user
        private static void WriteTaggedMessage(ConsoleColor errorColor, [NotNull] string tag, [NotNull] string message)
        {
            Console.ForegroundColor = errorColor;
            Console.Write(tag + " ");
            Console.ForegroundColor = ConsoleColor.Gray;
            Console.WriteLine(message);
        }
    }
}
