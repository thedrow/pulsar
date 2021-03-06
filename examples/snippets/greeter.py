import pulsar

names = ['john', 'luca', 'jo', 'alex']


@pulsar.command()
def greetme(request, message):
    echo = 'Hello {}!'.format(message['name'])
    request.actor.logger.info(echo)
    return echo


class Greeter:

    def __init__(self):
        cfg = pulsar.Config()
        cfg.parse_command_line()
        a = pulsar.arbiter(cfg=cfg)
        self.cfg = a.cfg
        self._loop = a._loop
        self._loop.call_later(1, pulsar.async, self())
        a.start()

    def __call__(self, a=None):
        if a is None:
            a = yield from pulsar.spawn(name='greeter')
        if names:
            name = names.pop()
            self._loop.logger.info("Hi! I'm %s" % name)
            yield from pulsar.send(a, 'greetme', {'name': name})
            self._loop.call_later(1, pulsar.async, self(a))
        else:
            pulsar.arbiter().stop()


if __name__ == '__main__':
    Greeter()
