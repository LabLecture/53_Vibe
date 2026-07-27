const WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;

export async function notify(title: string, body: string): Promise<boolean> {
  if (!WEBHOOK_URL) {
    console.error("DISCORD_WEBHOOK_URL이 .env에 설정되어 있지 않습니다.");
    return false;
  }

  try {
    const res = await fetch(WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        embeds: [{ title, description: body }],
      }),
    });

    if (!res.ok) {
      console.error(`Discord 웹훅 전송 실패: ${res.status} ${res.statusText}`);
      return false;
    }

    return true;
  } catch (err) {
    console.error("Discord 웹훅 요청 중 오류:", err);
    return false;
  }
}

if (import.meta.main) {
  const [title, body] = process.argv.slice(2);
  const finalTitle = title ?? "notify.ts 테스트";
  const finalBody = body ?? "기본 테스트 문구입니다.";

  const ok = await notify(finalTitle, finalBody);
  console.log(ok ? "전송 성공" : "전송 실패");
  process.exit(ok ? 0 : 1);
}
