Analysing INC-2043.

The incident has been raised at 19:38 on the 2026-08-12. The reporter says that the error happens in the payment page. 
We know we should only rely on factual evidence from the reporter and not his analysis of the problem, so it's reasonable to start by analysing checkout-service.log

Here we can see several  timeout errors while aqcuiring db pool conections
2026-08-12T19:34:12Z  checkout-service  ERROR  request failed method=POST path=/v2/checkout status=500 duration_ms=5021 error=PoolAcquireTimeout
2026-08-12T19:36:40Z  checkout-service  ERROR  timeout acquiring connection from pool=primary after 5000ms queue_depth=96 order_id=ord_88274

We can observer that the checkout-service that on the last succesful request, we already saturated the pool whose max value is 4
2026-08-12T19:31:49Z  checkout-service  INFO   request completed method=POST path=/v2/checkout status=200 duration_ms=168 pool_in_use=4 pool_max=4

However previously pool_max was set to a larget value
2026-08-12T19:20:03Z  checkout-service  INFO   request completed method=POST path=/v2/checkout status=200 duration_ms=142 pool_in_use=11 pool_max=40

We can see from postgres logs that the server still has plenty of spare connections. 

In platform events we can see that there has been a new checkout-service deployment just a little beofre the incident.

So the picture that comes out from this is that previously the service was running with a larger max number of pool connections and once it reached max number it started erroring.

From the changelog we can finally see that there had been a change that set max_pool to 4. 

The runbook tells us
2. If the pool size changed in the current release, roll the service back to the previous
   version per RB-010. Rollback is preferred over hot-patching configuration during an
   incident.

So the conclusion is to roll back to a previous version