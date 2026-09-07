import type { Metadata } from "next";
import { eq } from "drizzle-orm";
import { db } from "@/db";
import { orders, type Order, type OrderEvent } from "@/db/schema";
import { safeEqual } from "@/lib/orders";
import { rateLimit } from "@/lib/rate-limit";
import { clientKey } from "@/lib/origin";
import { Breadcrumbs, Field } from "@/components/ui/primitives";
import { OrderTimeline } from "@/components/account/order-timeline";
import { PackageIcon } from "@/components/icons";
export const metadata: Metadata = { title: "Suivre ma commande", robots: { index: false, follow: false } };
export const dynamic = "force-dynamic";
export default async function SuiviPage({ searchParams }: { searchParams: Promise<{ n?: string; e?: string; k?: string }> }) {
  const { n, e, k } = await searchParams;
  const number = n?.trim().toUpperCase();
  const email = e?.trim().toLowerCase();
  let order: (Order & { events: OrderEvent[] }) | null = null;
  let blocked = false;

  if (number && (email || k)) {
    // Throttled so the form cannot be used to enumerate order numbers.
    if (!(await rateLimit(`suivi:${await clientKey()}`, 20, 600_000))) {
      blocked = true;
    } else {
      const candidates = await db.query.orders.findMany({ where: eq(orders.number, number), with: { events: true }, limit: 1 });
      const candidate = candidates[0];
      if (candidate) {
        // Order number + a second factor: the verified e-mail, or the per-order
        // access key issued at checkout. The number alone is never sufficient.
        const byEmail = !!email && candidate.email.toLowerCase() === email;
        const byKey = safeEqual(k, candidate.accessKey);
        if (byEmail || byKey) order = candidate;
      }
    }
  }
  return (
    <div className="container-lux py-10 lg:py-14">
      <Breadcrumbs items={[{ label: "Suivi de commande" }]} />
      <div className="mx-auto mt-6 max-w-xl"><p className="eyebrow mb-4">Suivi</p><h1 className="font-display text-display-lg text-ink">Où en est ma commande ?</h1>
        <form className="mt-8 space-y-4"><Field label="Numéro de commande"><input name="n" defaultValue={n} placeholder="CL-241010-XXXX" required className="field" /></Field><Field label="E-mail utilisé"><input name="e" type="email" defaultValue={e} required className="field" /></Field><button className="btn-primary w-full">Suivre</button></form>
        {blocked && <p className="mt-6 text-sm text-error" role="alert">Trop de tentatives. Merci de réessayer dans quelques minutes.</p>}
        {!blocked && number && email && !order && <p className="mt-6 text-sm text-error" role="alert">Aucune commande trouvée avec ces informations.</p>}
        {order && <div className="mt-12 border border-stone bg-cream p-6"><div className="mb-6 flex items-center gap-3 text-ink"><PackageIcon size={20} className="text-champagne-2" /><span className="font-mono">{order.number}</span>{order.trackingCode && <span className="ml-auto text-xs text-muted">Suivi transporteur : {order.trackingCode}</span>}</div><OrderTimeline status={order.status} events={order.events} /></div>}
      </div>
    </div>
  );
}
