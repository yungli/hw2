# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')
        template = ncs.template.Template(service)
        vars = ncs.template.Variables()
        
        # check if the user input IP address is valid or not
        # get all the used IP addresses
        used_intf = []
        for device in root.devices:
            if device.device-type.cli.ned-id = "ios-id:cisco-ios":
                for intf in device.config.interface.GigabitEthernet:
                    used_intf.append(intf.ip.address.primary.address.split('.')[3])
            else:
                for intf in device.config.interface.GigabitEthernet:
                    used_intf.append(intf.ipv4.address.ip.split('.')[3])

        for device in service.device:
            type = root.devices[device.name].device-type.cli.ned-id
            service-type = device.service-type

        #apply configuration into the corresponding template with validation check
            if type = "ios-id:cisco-ios" :
                if not re.match(r'0//[0-48]', device.interface):
                    raise Exception('the interface format is invalid.')
                #if dns is appointed, apply all configuration into the template,otherwise, do nothing
                if device.dns:
                    vars.add('name', device.name)
                    vars.add('dns', device.dns)
                    vars.add('intf', device.interface)
                    if service-type = 'static-ip':
                        sub_ip = device.ip-address.split('.')[3]
                        if sub_ip in used_intf:
                           raise Exception('the sub-ip address has already been used!')
                        else:
                           used_intf.append(sub_ip)
                           vars.add('static-ip', device.ip-address)
                           vars.add('gateway', device.default-gateway)
                           template.apply('cisco-ios', vars)
           
            else:
                if not re.match(r'0//0//0//[0-48]', device.interface):
                    raise Exception('the interface format is invalid.')
                #if dns is appointed, apply all configuration into the template,otherwise, do nothing
                if device.dns:
                    vars.add('name', device.name)
                    vars.add('dns', device.dns)
                    vars.add('intf', device.interface)
                    if service-type = 'static-ip':
                        sub_ip = device.ip-address.split('.')[3]
                        if sub_ip in used_intf:
                           raise Exception('the sub-ip address has already been used!')
                        else:
                           used_intf.append(sub_ip)
                           vars.add('static-ip', device.ip-address)
                           vars.add('gateway', device.default-gateway)
                           template.apply('cisco-iosxe', vars)      

        

    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('hw-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
