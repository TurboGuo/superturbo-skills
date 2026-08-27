# Research plan

Eight to fourteen searches, in three layers, both languages. Stop when new searches
stop producing new traps.

## Layer 1, official. Do this first and completely

Find and read, in this order:

1. The official site, to establish the official name, the regional variants and their
   domains
2. The download or get started page, for system requirements and platform support
3. The documentation troubleshooting or FAQ section, which often contains the error
   code table nobody else reproduces
4. The changelog or release notes, for the current version number
5. The pricing page, for the free tier limit and what the paid tiers unlock

Version, system requirements, price and free tier limits are recorded from these
pages only. If a page does not state one, the manual says "not stated on the official
page". It does not borrow the number from a blog.

Query shapes:

- `<tool> official documentation troubleshooting`
- `<tool> system requirements download page`
- `<tool> pricing free tier limits`
- `<tool> changelog latest version`
- `<tool> 官方文档 常见问题`

## Layer 2, official community

The official forum, GitHub issues, official help threads. This layer produces the
error codes and the failures that recur, which is the highest value material in the
whole manual and the material least likely to appear in a tutorial.

Query shapes:

- `<tool> forum error code connection failed`
- `<tool> github issues install fails`
- `<tool> 官方论坛 报错 解决`
- `site:<official forum domain> <symptom>`

## Layer 3, public experience

Blogs, tutorials, community sites, video transcripts. Everything here is second hand
until proven otherwise.

Search both languages every time. The Chinese and English user bases of the same tool
hit different walls, because regional builds, default models and network conditions
differ. A manual built from one side only is missing half the traps.

Query shapes:

- `<tool> beginner mistakes what I wish I knew`
- `<tool> setup problems fixed`
- `<tool> 踩坑 新手 避坑指南`
- `<tool> 安装失败 解决方法`
- `<tool> <specific symptom the client reported>`

If the client reported a symptom during intake, that symptom gets its own search
before anything else in this layer.

## When the tool is obscure

New tools and small tools produce almost nothing in layers 2 and 3. That is a finding,
not a failure, and it is where this manual is worth the most, because no static guide
exists to compete with it.

In that case: read the official documentation more thoroughly, cover the stages from
first principles, and say plainly in the header that public experience is thin and the
manual will grow as the client uses the tool.

Never pad a thin result with traps borrowed from a similar tool. A trap from a
different product presented as this product's trap is a fabrication.

## What not to research

Methods for reaching a service from a region where its operator does not offer it.
Record the official availability statement and the officially available alternatives
in that region, and stop there.
