import hashlib
import re
import base64

from redbot.core import commands
from redbot.core.utils.chat_formatting import pagify

from typing import Optional
from string import ascii_lowercase as lc, ascii_uppercase as uc

from .braille import (
    letters,
    r_letters,
    contractions,
    r_contractions,
    punctuation,
    r_punctuation,
    numbers,
    r_numbers,
)


class Encoding(commands.Cog):
    """
        Convert messages into fun encodings
    """

    __author__ = ["TrustyJAID"]
    __version__ = "1.2.0"

    def __init__(self, bot):
        self.bot = bot
        self.table = {
            "A": [
                "00",
                "01",
                "10",
                "11",
                "00",
                "00",
                "00",
                "01",
                "01",
                "01",
                "10",
                "10",
                "10",
                "11",
                "11",
                "11",
            ],
            "G": [
                "01",
                "10",
                "11",
                "00",
                "11",
                "10",
                "01",
                "11",
                "00",
                "10",
                "11",
                "00",
                "01",
                "00",
                "01",
                "10",
            ],
            "C": [
                "10",
                "11",
                "00",
                "01",
                "10",
                "11",
                "10",
                "10",
                "11",
                "00",
                "01",
                "11",
                "00",
                "01",
                "00",
                "01",
            ],
            "T": [
                "11",
                "00",
                "01",
                "10",
                "01",
                "01",
                "11",
                "00",
                "10",
                "11",
                "00",
                "01",
                "11",
                "10",
                "10",
                "00",
            ],
        }
        # A = 00
        # G = 10
        # C = 11
        # T = 01

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
            Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    def search_words(self, data: str) -> bool:
        count = 0
        try:
            for char in data:
                if ord(char) in range(47, 122):
                    count += 1
        except TypeError:
            for char in data:
                if char in range(47, 122):
                    count += 1
        try:
            if (count / len(data)) >= 0.75:
                return True
        except ZeroDivisionError:
            return False
        return False

    @commands.group(name="hash")
    async def hash_cmd(self, ctx: commands.Context) -> None:
        """Various hashing commands"""
        pass

    @hash_cmd.group(name="md5")
    async def hash_md5(self, ctx: commands.Context, *, txt: str) -> None:
        """
            MD5 Encrypt Text
        """
        md5 = hashlib.md5(txt.encode()).hexdigest()
        await ctx.send("**MD5**\n" + md5)

    @hash_cmd.command(name="sha1")
    async def hash_sha1(self, ctx: commands.Context, *, txt: str) -> None:
        """
            SHA1 Encrypt Text
        """
        sha = hashlib.sha1(txt.encode()).hexdigest()
        await ctx.send("**SHA1**\n" + sha)

    @hash_cmd.command(name="sha256")
    async def hash_sha256(self, ctx: commands.Context, *, txt: str) -> None:
        """
            SHA256 Encrypt Text
        """
        sha256 = hashlib.sha256(txt.encode()).hexdigest()
        await ctx.send("**SHA256**\n" + sha256)

    @hash_cmd.command(name="sha512")
    async def hash_sha512(self, ctx: commands.Context, *, txt: str) -> None:
        """
            SHA512 Encrypt Text
        """
        sha512 = hashlib.sha512(txt.encode()).hexdigest()
        await ctx.send("**SHA512**\n" + sha512)

    @commands.group(name="encode")
    async def _encode(self, ctx: commands.Context) -> None:
        """Encode a string."""
        pass

    @commands.group(name="decode")
    async def _decode(self, ctx: commands.Context) -> None:
        """Decode a string."""
        pass

    @_encode.command(name="binary")
    async def encode_binary(self, ctx: commands.Context, *, message: str) -> None:
        """
            Encode text into binary sequences of 8
        """
        ascii_bin = " ".join(bin(x)[2:].zfill(8) for x in message.encode("utf-8"))
        await ctx.send(ascii_bin)

    @_decode.command(name="binary")
    async def decode_binary(self, ctx: commands.Context, *, message: str) -> None:
        """
            Decode binary sequences of 8
        """
        msg = message.replace(" ", "")
        bin_ascii = "".join([chr(int(msg[i : i + 8], 2)) for i in range(0, len(msg), 8)])
        await ctx.send(bin_ascii)

    @_encode.command(name="hex")
    async def encode_hex(self, ctx: commands.Context, *, message: str) -> None:
        """
            Encode text into hexadecimal
        """
        ascii_bin = " ".join(hex(x)[2:] for x in message.encode("utf-8"))
        await ctx.send(ascii_bin)

    @_decode.command(name="hex")
    async def decode_hex(self, ctx: commands.Context, *, message: str) -> None:
        """
            Decode a hexadecimal sequence to text
        """
        ascii_bin = "".join(chr(int("0x" + x, 16)) for x in re.split(r"[\s]+", message))
        await ctx.send(ascii_bin)

    @_encode.command(name="b64", aliases=["base64"])
    async def encode_b64(self, ctx: commands.Context, *, message: str) -> None:
        """
            Encode text into base 64
        """
        await ctx.send(base64.b64encode(bytes(message, "utf-8")).decode("utf-8"))

    @_decode.command(name="b64", aliases=["base64"])
    async def decode_b64(self, ctx: commands.Context, *, message: str) -> None:
        """
            Decode a base 64 text
        """
        await ctx.send(base64.b64decode(bytes(message, "utf-8")).decode("utf-8"))

    @_encode.command(name="chr", aliases=["character"])
    async def encode_char(self, ctx: commands.Context, *, message: str) -> None:
        """
            Encode message into character numbers
        """
        await ctx.send(" ".join(str(ord(x)) for x in message))

    @_decode.command(name="chr", aliases=["character"])
    async def decode_char(self, ctx: commands.Context, *, message: str) -> None:
        """
            Decode character numbers to a message
        """
        await ctx.send(" ".join(str(chr(int(x))) for x in re.split(r"[\s]+", message)))

    @_encode.command(name="braille")
    async def encode_braille(self, ctx: commands.Context, *, message: str) -> None:
        """
            Encode text into braille unicode characters
        """
        for word in re.split(r"[\s]+", message):
            if word.lower() in contractions:
                message = message.replace(word, contractions[word.lower()])
        for letter in message:
            if letter.isdigit():
                message = message.replace(letter, chr(10300) + numbers[letter])
            if letter.isupper():
                message = message.replace(letter, chr(10272) + letters[letter.lower()])
            if letter in letters:
                message = message.replace(letter, letters[letter])
            if letter in punctuation:
                message = message.replace(letter, punctuation[letter])
        await ctx.send(message)

    @_decode.command(name="braille")
    async def decode_braille(self, ctx: commands.Context, *, message: str) -> None:
        """
            Decide braille unicode characters to ascii
        """
        for word in re.split(r"[\s]+", message):
            if word in r_contractions:
                message = message.replace(word, r_contractions[word])
        replacement = ""
        for letter in message:
            if letter == chr(10300):
                replacement = "number"
                continue
            if letter == chr(10272):
                replacement = "capital"
                continue
            if replacement == "number":
                message = message.replace(chr(10300) + letter, r_numbers[letter])
                replacement = ""
                continue
            if replacement == "capital":
                message = message.replace(chr(10272) + letter, r_letters[letter].upper())
                replacement = ""
                continue
        for letter in message:
            if letter in r_punctuation:
                message = message.replace(letter, r_punctuation[letter])
            if letter in r_letters:
                message = message.replace(letter, r_letters[letter])

        await ctx.send(message[:2000])

    def rot_encode(self, n: int, text: str) -> str:
        """
            https://stackoverflow.com/questions/47580337/short-rot-n-decode-function-in-python
        """
        lookup = str.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
        return text.translate(lookup)

    @_encode.command(name="rot", aliases=["caeser"])
    async def caeser_encode(
        self, ctx: commands.Context, rot_key: Optional[int], *, message: str
    ) -> None:
        """
            Encode a caeser cipher message with specified key
        """
        if not rot_key:
            rot_key = 13
        await ctx.send(self.rot_encode(rot_key, message))

    @_decode.command(name="rot", aliases=["caeser"])
    async def caeser_decode(
        self, ctx: commands.Context, rot_key: Optional[int], *, message: str
    ) -> None:
        """
            Decode a caeser cipher message with specified key
        """
        if not rot_key:
            rot_key = 13
        await ctx.send(self.rot_encode(-rot_key, message))

    @_encode.command(name="dna")
    async def dna_encode(self, ctx: commands.Context, *, message: str) -> None:
        """
            Encodes a string into DNA 4 byte ACGT format
        """
        dna = {"00": "A", "01": "T", "10": "G", "11": "C"}
        message = message.strip(" ")
        binary = " ".join(bin(x)[2:].zfill(8) for x in message.encode("utf-8")).replace(" ", "")
        binlist = [binary[i: i + 2] for i in range(0, len(binary), 2)]
        newmsg = ""
        count = 0
        for letter in binlist:
            newmsg += dna[letter]
            count += 1
            if count == 4:
                count = 0
                newmsg += " "
        await ctx.send(newmsg)

    @_decode.command(name="dna")
    async def dna_decode(self, ctx: commands.Context, *, message: str) -> None:
        """
            Decodes a string of DNA in 4 byte ACGT format.
        """
        message = message.strip(" ")
        mapping = {}
        replacement = ""
        for i in range(0, 16):
            skip = [" ", "\n", "\r"]
            for character in message:
                if character in skip:
                    continue
                replacement += self.table[character][i]
            try:
                n = int("0b" + replacement, 2)
                mapping[i] = n.to_bytes((n.bit_length() + 7) // 8, "big").decode("utf8", "ignore")
            except TypeError:
                pass
            replacement = ""
        num = 1
        new_msg = "Possible solutions:\n"
        for result in mapping.values():
            new_msg += str(num) + ": " + result + "\n"
            num += 1
        for page in pagify(new_msg, shorten_by=20):
            await ctx.send(f"```\n{page}\n```")
