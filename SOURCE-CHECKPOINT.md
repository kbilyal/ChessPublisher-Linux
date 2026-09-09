# Shared Source Checkpoint — v1.06.00-beta.85 target

Status: **AUTHORITATIVE IDENTITY PINNED / HOSTED PLATFORM PASS / EXACT-SOURCE MATERIALIZATION PENDING**
Date: 2026-09-10

## Authoritative beta.85 source
- Windows repository: `kbilyal/Chess-Publisher-Windows-FIDE-Beta`
- source commit: `1354a8061fbbc520ecd1ea09b93350e388428dfd`
- archive: `Chess-Publisher-Windows-v1.06.00-beta.85-AUTHORITATIVE-SOURCE.tar.gz`
- archive SHA256: `2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69`
- archive metadata size: `27933592` bytes
- internal version target: `1.06.00-beta.85`
- Linux source snapshot identity: `cp-v1.06.00-beta.85-shared-source-20260909`
- Cloud fingerprint content schema: 7

The Linux source manifest pins the authoritative cumulative changed shared hashes. The Linux materializer accepts only the exact beta.85 archive/root and only copies manifest-listed shared files; Windows launchers/binaries are not part of the Linux shared-source payload.

## Hosted platform proof
At accepted hosted commit `a19155fa2002d8175f3db4ba046cdba903d172bf`:
- Platform Acceptance #42 (`34406223149`): PASS
- Cross-Platform Parity #38 (`34406223165`): PASS
- Rating Lists #16 (`34406223143`): PASS
- Web Results #10 (`34406223189`): PASS
- protected core modified by beta.85 Linux alignment: NO

Platform-only artifact: `chess-publisher-linux-beta85-platform-only-kit`, ID `10125532864`, digest `sha256:ef9ee9136b79bf86f15f52265b20f987a4ab6e1734bb24314f4513b08103fe35`.

## Blocked exact-source proof
The authoritative archive is visible in the connected Google Drive beta85 release folder, but raw download/materialization through the connected provider returns HTTP 403 because the provider flags the archive/binary. This is an external access block, not converted into product PASS evidence.

Therefore beta.85 exact shared-source byte identity, exact-source package acceptance and beta.85 `.deb` are still pending. `releaseCandidate` remains false.

## Previous exact-source anchor
beta.81 remains the last fully proven exact-source parity anchor:
- 574/574 shared files byte-identical
- 20/20 Windows/Linux matrix PASS
- Linux commit `30c6b924e11b9ebcd1ef2337761640c02cc1e580`
- Platform Acceptance `34384400988` PASS
- beta.81 package SHA256 `be2015aec5b1f64490cd1496ffe2323bbadf898285007f8afdca00c48c29addc`

## Next gate
Obtain readable beta.85 archive bytes, verify `2795a061...`, materialize and verify every manifest-listed shared file, rerun exact-source regression/package gates, build the beta.85 `.deb`, and then require real Ubuntu installation/start confirmation.
