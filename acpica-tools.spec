Name:           acpica-tools
Version:        20210604
Release:        3
Summary:        Tools for OS-independent reference implementation of ACPI

License:        GPLv2
URL:            https://www.acpica.org/

Source0:        https://acpica.org/sites/acpica/files/acpica-unix2-%{version}.tar.gz
Source1:        https://acpica.org/sites/acpica/files/acpitests-unix-%{version}.tar.gz
Source2:        COPYING

Patch0001:      cve-2017-13693.patch
Patch0002:      cve-2017-13694.patch
Patch0003:      cve-2017-13695.patch
Patch0004:      openEuler-harden.patch
Patch0005:      acpica-unix2-20210604-sw.patch
Patch0006:	acpica-unix2-20210604-loongarch64.patch

BuildRequires:  bison patchutils flex gcc
Provides:       acpixtract >= 20120913-7 iasl = %{version}-%{release} acpidump >= 20100513-5
Provides:       pmtools = %{version}-%{release}
Obsoletes:      iasl < 20120913-8 pmtools < 20100513-6

%description
The ACPI Component Architecture (ACPICA) project provides an operating system (OS)-independent
reference implementation of the Advanced Configuration and Power Interface Specification (ACPI).
It can be easily adapted to execute under any host OS. The ACPICA code is meant to be directly
integrated into the host OS as a kernel-resident subsystem. Hosting the ACPICA subsystem requires
no changes to the core ACPICA code. Instead, a small OS-specific interface layer is written
specifically for each host OS in order to interface the ACPICA code to the native OS services.
The complexity of the ACPI specification leads to a lengthy and difficult implementation in
operating system software. The primary purpose of the ACPI Component Architecture is to simplify
ACPI implementations for operating system vendors (OSVs) by providing major portions of an ACPI
implementation in OS-independent ACPI modules that can be easily integrated into any OS.

%prep
%autosetup -n acpica-unix2-%{version} -p1
gzip -dc %{SOURCE1} | tar -x --strip-components=1 -f -

install -p %{SOURCE2} COPYING

chmod a-x changes.txt
chmod a-x source/compiler/new_table.txt

%build
CWARNINGFLAGS="\
    -std=c99 -Wall -Wbad-function-cast -Wdeclaration-after-statement -Werror -Wformat=2\
    -Wmissing-declarations -Wmissing-prototypes -Wstrict-aliasing=0 -Wstrict-prototypes\
    -Wswitch-default -Wpointer-arith -Wundef -Waddress -Waggregate-return -Winit-self\
    -Winline -Wmissing-declarations -Wmissing-field-initializers -Wnested-externs\
    -Wold-style-definition -Wno-format-nonliteral -Wredundant-decls -Wempty-body\
    -Woverride-init -Wlogical-op -Wmissing-parameter-type -Wold-style-declaration\
    -Wtype-limits"

export OPT_CFLAGS="%{optflags} $CWARNINGFLAGS"
export OPT_LDFLAGS="%{__global_ldflags}"

%make_build

%install
install -d %{buildroot}%{_bindir}
install -pD generate/unix/bin*/* %{buildroot}%{_bindir}/

install -d %{buildroot}%{_docdir}/acpica-tools/examples
install -pDm 0644 source/tools/examples/* %{buildroot}%{_docdir}/acpica-tools/examples/

%pre
if [ -e %{_bindir}/acpixtract-acpica ];then
    alternatives --remove acpixtract %{_bindir}/acpixtract-acpica
fi
if [ -e %{_bindir}/acpidump-acpica ];then
    alternatives --remove acpidump %{_bindir}/acpidump-acpica
fi

%postun
if [ -e %{_bindir}/acpixtract-acpica ];then
    alternatives --remove acpixtract %{_bindir}/acpixtract-acpica
fi
if [ -e %{_bindir}/acpidump-acpica ];then
    alternatives --remove acpidump %{_bindir}/acpidump-acpica
fi

%files
%doc changes.txt source/compiler/new_table.txt COPYING
%{_bindir}/*
%{_docdir}/*

%changelog
* Wed Aug 17 2022 mahailiang <mahailiang@uniontech.com> - 20210604-3
- add loongarch64 support

* Wed Jul 20 2022 wuzx<wuzx1226@qq.com> - 20210604-2
- add sw64 patch

* Wed Dec 30 2021 zhouwenpei <zhouwenpei1@huawei.com> - 20210604-1
- Upgrade to version 20210604

* Sat Jan 30 2021 xinghe <xinghe1@huawei.com> - 20210105-1
- Upgrade to version 20210105

* Wed Jul 22 2020 jinzhimin <jinzhimin2@huawei.com> - 20200528-1
- update to 20200528

* Tue Dec 31 2019 daiqianwen <daiqianwen@huawei.com> - 20190509-4
- Package init
