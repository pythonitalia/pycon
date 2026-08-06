import { AppSidebar } from "@/components/app-sidebar";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { TooltipProvider } from "@/components/ui/tooltip";

export default function Dashboard() {
  return (
    <TooltipProvider>
      <SidebarProvider className="antialiased">
        <AppSidebar />
        <SidebarInset className="isolate min-h-dvh">
          <header className="flex h-14 shrink-0 items-center gap-2 border-b px-4">
            <SidebarTrigger />
            <Separator
              className="data-vertical:h-4 data-vertical:self-auto"
              orientation="vertical"
            />
            <h1 className="text-base font-medium">Dashboard</h1>
          </header>
          <div className="p-8">
            <h2 className="text-4xl font-bold tracking-tight">Hello</h2>
          </div>
        </SidebarInset>
      </SidebarProvider>
    </TooltipProvider>
  );
}
