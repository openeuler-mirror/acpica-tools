Name:           acpica-tools
Version:        20190509
Release:        4
Summary:        Tools for OS-independent reference implementation of ACPI

License:        GPLv2
URL:            https://www.acpica.org/

Source0:        https://acpica.org/sites/acpica/files/acpica-unix2-%{version}.tar.gz
Source1:        https://acpica.org/sites/acpica/files/acpitests-unix-%{version}.tar.gz
Source2:        iasl.1
Source3:        acpibin.1
Source4:        acpidump.1
Source5:        acpiexec.1
Source6:        acpihelp.1
Source7:        acpinames.1
Source8:        acpisrc.1
Source9:        acpixtract.1
Source10:       acpiexamples.1
Source11:       badcode.asl.result
Source12:       grammar.asl.result
Source13:       converterSample.asl.result
Source14:       run-misc-tests.sh
Source15:       COPYING

Patch0001:      big-endian.patch
Patch0002:      unaligned.patch
Patch0003:      OPT_LDFLAGS.patch
Patch0004:      int-format.patch
Patch0005:      f23-harden.patch
Patch0006:      template.patch
Patch0007:      ppc64le.patch
Patch0008:      arm7hl.patch
Patch0009:      big-endian-v2.patch
Patch0010:      simple-64bit.patch
Patch0011:      mips-be-fix.patch
Patch0012:      cve-2017-13693.patch
Patch0013:      cve-2017-13694.patch
Patch0014:      cve-2017-13695.patch
Patch0015:      str-trunc-warn.patch
Patch0016:      ptr-cast.patch
Patch0017:      aslcodegen.patch
Patch0018:      facp.patch

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

%package help
Summary:        Help documantation of acpica-tools package

%description help
Help documantation of acpica-tools package.

%prep
%autosetup -n acpica-unix2-%{version} -p1
gzip -dc %{SOURCE1} | tar -x --strip-components=1 -f -

install -p %{SOURCE2} iasl.1
install -p %{SOURCE3} acpibin.1
install -p %{SOURCE4} acpidump.1
install -p %{SOURCE5} acpiexec.1
install -p %{SOURCE6} acpihelp.1
install -p %{SOURCE7} acpinames.1
install -p %{SOURCE8} acpisrc.1
install -p %{SOURCE9} acpixtract.1
install -p %{SOURCE10} acpiexamples.1
install -p %{SOURCE11} badcode.asl.result
install -p %{SOURCE12} grammar.asl.result
install -p %{SOURCE13} converterSample.asl.result
install -p %{SOURCE14} tests/run-misc-tests.sh
install -p %{SOURCE15} COPYING

chmod a+x tests/run-misc-tests.sh
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

install -d %{buildroot}%{_mandir}/man1
install -pDm 0644 *.1 %{buildroot}%{_mandir}/man1/

install -d %{buildroot}%{_docdir}/acpica-tools/examples
install -pDm 0644 source/tools/examples/* %{buildroot}%{_docdir}/acpica-tools/examples/

%check
cd tests

./aslts.sh
[ $? -eq 0 ] || exit 1

./run-misc-tests.sh %{buildroot}%{_bindir} %{version}

cd templates
make
if [ -f diff.log ];then
    if [ -s diff.log ];then
        exit 1
    fi
fi
cd ..

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

%files help
%{_mandir}/*
%{_docdir}/*

%changelog
* Tue Dec 31 2019 daiqianwen <daiqianwen@huawei.com> - 20190509-4
- Package init
