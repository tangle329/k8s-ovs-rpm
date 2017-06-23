%global debug_package   %{nil}
%global provider        github
%global provider_tld    com
%global project         tangle
%global repo            k8s-ovs
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

%global devel_main      k8s-ovs-devel

Name:           k8s-ovs
Version:        0.1.0
Release:        1%{?dist}
Summary:        kubernetes openvswitch SDN
License:        GPL
URL:            https://%{import_path}
Source0:        k8s-ovs-%{version}.tar.gz
Source1:        k8s-ovs.service
Source2:        k8s-ovs

ExclusiveArch:  %{ix86} x86_64 %{arm}

BuildRequires:      golang >= 1.6.0
BuildRequires:      pkgconfig(systemd)

Requires:           openvswitch >= 2.5.0
Requires:           openvswitch-kmod >= 2.5.0
Requires:           systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
k8s-ovs is a SDN system for kubernetes. 

%prep
%setup -q -n %{repo}

%build
mkdir -p src/
ln -s ../ src/k8s-ovs

export GOPATH=$(pwd)
go build -o rootfs/opt/cni/bin/k8s-ovs k8s-ovs/cniclient
go build -o rootfs/usr/sbin/k8s-ovs k8s-ovs

%install
install -D -p -m 755 rootfs/opt/cni/bin/k8s-ovs %{buildroot}/opt/cni/bin/k8s-ovs
install -D -p -m 755 rootfs/opt/cni/bin/host-local  %{buildroot}/opt/cni/bin/host-local
install -D -p -m 755 rootfs/opt/cni/bin/loopback %{buildroot}/opt/cni/bin/loopback
install -D -p -m 755 rootfs/usr/sbin/k8s-ovs %{buildroot}/usr/sbin/k8s-ovs
install -D -p -m 755 rootfs/usr/sbin/k8s-sdn-ovs %{buildroot}/usr/sbin/k8s-sdn-ovs
install -D -p -m 644 rootfs/etc/cni/net.d/80-k8s-ovs.conf %{buildroot}/etc/cni/net.d/80-k8s-ovs.conf
install -D -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/k8s-ovs.service
install -D -p -m 644 %{SOURCE2} %{buildroot}/etc/sysconfig/k8s-ovs

%post
%systemd_post k8s-ovs.service

%preun
# clean tempdir and workdir on removal or upgrade
%systemd_preun k8s-ovs.service

%postun
%systemd_postun_with_restart k8s-ovs.service

%files
/opt/cni/bin/k8s-ovs
/opt/cni/bin/host-local
/opt/cni/bin/loopback
/usr/sbin/k8s-ovs
/usr/sbin/k8s-sdn-ovs
/etc/cni/net.d/80-k8s-ovs.conf
%{_unitdir}/k8s-ovs.service
/etc/sysconfig/k8s-ovs
