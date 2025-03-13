# pydantic_ai.agent

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.agent

```
pydantic_ai.agent
```

[](https://ai.pydantic.dev)

### Agent

dataclass

```
dataclass
```

Bases: Generic[AgentDepsT, ResultDataT]

```
Generic[AgentDepsT, ResultDataT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

Class for defining "agents" - a way to have a specific type of "conversation" with an LLM.

Agents are generic in the dependency type they take AgentDepsT
and the result data type they return, ResultDataT.

```
AgentDepsT
```

```
ResultDataT
```

By default, if neither generic parameter is customised, agents have type Agent[None, str].

```
Agent[None, str]
```

Minimal usage example:

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')
result = agent.run_sync('What is the capital of France?')
print(result.data)
#> Paris
```

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')
result = agent.run_sync('What is the capital of France?')
print(result.data)
#> Paris
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
70
  71
  72
  73
  74
  75
  76
  77
  78
  79
  80
  81
  82
  83
  84
  85
  86
  87
  88
  89
  90
  91
  92
  93
  94
  95
  96
  97
  98
  99
 100
 101
 102
 103
 104
 105
 106
 107
 108
 109
 110
 111
 112
 113
 114
 115
 116
 117
 118
 119
 120
 121
 122
 123
 124
 125
 126
 127
 128
 129
 130
 131
 132
 133
 134
 135
 136
 137
 138
 139
 140
 141
 142
 143
 144
 145
 146
 147
 148
 149
 150
 151
 152
 153
 154
 155
 156
 157
 158
 159
 160
 161
 162
 163
 164
 165
 166
 167
 168
 169
 170
 171
 172
 173
 174
 175
 176
 177
 178
 179
 180
 181
 182
 183
 184
 185
 186
 187
 188
 189
 190
 191
 192
 193
 194
 195
 196
 197
 198
 199
 200
 201
 202
 203
 204
 205
 206
 207
 208
 209
 210
 211
 212
 213
 214
 215
 216
 217
 218
 219
 220
 221
 222
 223
 224
 225
 226
 227
 228
 229
 230
 231
 232
 233
 234
 235
 236
 237
 238
 239
 240
 241
 242
 243
 244
 245
 246
 247
 248
 249
 250
 251
 252
 253
 254
 255
 256
 257
 258
 259
 260
 261
 262
 263
 264
 265
 266
 267
 268
 269
 270
 271
 272
 273
 274
 275
 276
 277
 278
 279
 280
 281
 282
 283
 284
 285
 286
 287
 288
 289
 290
 291
 292
 293
 294
 295
 296
 297
 298
 299
 300
 301
 302
 303
 304
 305
 306
 307
 308
 309
 310
 311
 312
 313
 314
 315
 316
 317
 318
 319
 320
 321
 322
 323
 324
 325
 326
 327
 328
 329
 330
 331
 332
 333
 334
 335
 336
 337
 338
 339
 340
 341
 342
 343
 344
 345
 346
 347
 348
 349
 350
 351
 352
 353
 354
 355
 356
 357
 358
 359
 360
 361
 362
 363
 364
 365
 366
 367
 368
 369
 370
 371
 372
 373
 374
 375
 376
 377
 378
 379
 380
 381
 382
 383
 384
 385
 386
 387
 388
 389
 390
 391
 392
 393
 394
 395
 396
 397
 398
 399
 400
 401
 402
 403
 404
 405
 406
 407
 408
 409
 410
 411
 412
 413
 414
 415
 416
 417
 418
 419
 420
 421
 422
 423
 424
 425
 426
 427
 428
 429
 430
 431
 432
 433
 434
 435
 436
 437
 438
 439
 440
 441
 442
 443
 444
 445
 446
 447
 448
 449
 450
 451
 452
 453
 454
 455
 456
 457
 458
 459
 460
 461
 462
 463
 464
 465
 466
 467
 468
 469
 470
 471
 472
 473
 474
 475
 476
 477
 478
 479
 480
 481
 482
 483
 484
 485
 486
 487
 488
 489
 490
 491
 492
 493
 494
 495
 496
 497
 498
 499
 500
 501
 502
 503
 504
 505
 506
 507
 508
 509
 510
 511
 512
 513
 514
 515
 516
 517
 518
 519
 520
 521
 522
 523
 524
 525
 526
 527
 528
 529
 530
 531
 532
 533
 534
 535
 536
 537
 538
 539
 540
 541
 542
 543
 544
 545
 546
 547
 548
 549
 550
 551
 552
 553
 554
 555
 556
 557
 558
 559
 560
 561
 562
 563
 564
 565
 566
 567
 568
 569
 570
 571
 572
 573
 574
 575
 576
 577
 578
 579
 580
 581
 582
 583
 584
 585
 586
 587
 588
 589
 590
 591
 592
 593
 594
 595
 596
 597
 598
 599
 600
 601
 602
 603
 604
 605
 606
 607
 608
 609
 610
 611
 612
 613
 614
 615
 616
 617
 618
 619
 620
 621
 622
 623
 624
 625
 626
 627
 628
 629
 630
 631
 632
 633
 634
 635
 636
 637
 638
 639
 640
 641
 642
 643
 644
 645
 646
 647
 648
 649
 650
 651
 652
 653
 654
 655
 656
 657
 658
 659
 660
 661
 662
 663
 664
 665
 666
 667
 668
 669
 670
 671
 672
 673
 674
 675
 676
 677
 678
 679
 680
 681
 682
 683
 684
 685
 686
 687
 688
 689
 690
 691
 692
 693
 694
 695
 696
 697
 698
 699
 700
 701
 702
 703
 704
 705
 706
 707
 708
 709
 710
 711
 712
 713
 714
 715
 716
 717
 718
 719
 720
 721
 722
 723
 724
 725
 726
 727
 728
 729
 730
 731
 732
 733
 734
 735
 736
 737
 738
 739
 740
 741
 742
 743
 744
 745
 746
 747
 748
 749
 750
 751
 752
 753
 754
 755
 756
 757
 758
 759
 760
 761
 762
 763
 764
 765
 766
 767
 768
 769
 770
 771
 772
 773
 774
 775
 776
 777
 778
 779
 780
 781
 782
 783
 784
 785
 786
 787
 788
 789
 790
 791
 792
 793
 794
 795
 796
 797
 798
 799
 800
 801
 802
 803
 804
 805
 806
 807
 808
 809
 810
 811
 812
 813
 814
 815
 816
 817
 818
 819
 820
 821
 822
 823
 824
 825
 826
 827
 828
 829
 830
 831
 832
 833
 834
 835
 836
 837
 838
 839
 840
 841
 842
 843
 844
 845
 846
 847
 848
 849
 850
 851
 852
 853
 854
 855
 856
 857
 858
 859
 860
 861
 862
 863
 864
 865
 866
 867
 868
 869
 870
 871
 872
 873
 874
 875
 876
 877
 878
 879
 880
 881
 882
 883
 884
 885
 886
 887
 888
 889
 890
 891
 892
 893
 894
 895
 896
 897
 898
 899
 900
 901
 902
 903
 904
 905
 906
 907
 908
 909
 910
 911
 912
 913
 914
 915
 916
 917
 918
 919
 920
 921
 922
 923
 924
 925
 926
 927
 928
 929
 930
 931
 932
 933
 934
 935
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
```

```
@final
@dataclasses.dataclass(init=False)
class Agent(Generic[AgentDepsT, ResultDataT]):
    """Class for defining "agents" - a way to have a specific type of "conversation" with an LLM.

    Agents are generic in the dependency type they take [`AgentDepsT`][pydantic_ai.tools.AgentDepsT]
    and the result data type they return, [`ResultDataT`][pydantic_ai.result.ResultDataT].

    By default, if neither generic parameter is customised, agents have type `Agent[None, str]`.

    Minimal usage example:

    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')
    result = agent.run_sync('What is the capital of France?')
    print(result.data)
    #> Paris
    ```
    """

    # we use dataclass fields in order to conveniently know what attributes are available
    model: models.Model | models.KnownModelName | None
    """The default model configured for this agent."""

    name: str | None
    """The name of the agent, used for logging.

    If `None`, we try to infer the agent name from the call frame when the agent is first run.
    """
    end_strategy: EndStrategy
    """Strategy for handling tool calls when a final result is found."""

    model_settings: ModelSettings | None
    """Optional model request settings to use for this agents's runs, by default.

    Note, if `model_settings` is provided by `run`, `run_sync`, or `run_stream`, those settings will
    be merged with this value, with the runtime argument taking priority.
    """

    result_type: type[ResultDataT] = dataclasses.field(repr=False)
    """
    The type of the result data, used to validate the result data, defaults to `str`.
    """

    instrument: InstrumentationSettings | bool | None
    """Options to automatically instrument with OpenTelemetry."""

    _instrument_default: ClassVar[InstrumentationSettings | bool] = False

    _deps_type: type[AgentDepsT] = dataclasses.field(repr=False)
    _result_tool_name: str = dataclasses.field(repr=False)
    _result_tool_description: str | None = dataclasses.field(repr=False)
    _result_schema: _result.ResultSchema[ResultDataT] | None = dataclasses.field(repr=False)
    _result_validators: list[_result.ResultValidator[AgentDepsT, ResultDataT]] = dataclasses.field(repr=False)
    _system_prompts: tuple[str, ...] = dataclasses.field(repr=False)
    _system_prompt_functions: list[_system_prompt.SystemPromptRunner[AgentDepsT]] = dataclasses.field(repr=False)
    _system_prompt_dynamic_functions: dict[str, _system_prompt.SystemPromptRunner[AgentDepsT]] = dataclasses.field(
        repr=False
    )
    _function_tools: dict[str, Tool[AgentDepsT]] = dataclasses.field(repr=False)
    _default_retries: int = dataclasses.field(repr=False)
    _max_result_retries: int = dataclasses.field(repr=False)
    _override_deps: _utils.Option[AgentDepsT] = dataclasses.field(default=None, repr=False)
    _override_model: _utils.Option[models.Model] = dataclasses.field(default=None, repr=False)

    def __init__(
        self,
        model: models.Model | models.KnownModelName | None = None,
        *,
        result_type: type[ResultDataT] = str,
        system_prompt: str | Sequence[str] = (),
        deps_type: type[AgentDepsT] = NoneType,
        name: str | None = None,
        model_settings: ModelSettings | None = None,
        retries: int = 1,
        result_tool_name: str = 'final_result',
        result_tool_description: str | None = None,
        result_retries: int | None = None,
        tools: Sequence[Tool[AgentDepsT] | ToolFuncEither[AgentDepsT, ...]] = (),
        defer_model_check: bool = False,
        end_strategy: EndStrategy = 'early',
        instrument: InstrumentationSettings | bool | None = None,
    ):
        """Create an agent.

        Args:
            model: The default model to use for this agent, if not provide,
                you must provide the model when calling it.
            result_type: The type of the result data, used to validate the result data, defaults to `str`.
            system_prompt: Static system prompts to use for this agent, you can also register system
                prompts via a function with [`system_prompt`][pydantic_ai.Agent.system_prompt].
            deps_type: The type used for dependency injection, this parameter exists solely to allow you to fully
                parameterize the agent, and therefore get the best out of static type checking.
                If you're not using deps, but want type checking to pass, you can set `deps=None` to satisfy Pyright
                or add a type hint `: Agent[None, <return type>]`.
            name: The name of the agent, used for logging. If `None`, we try to infer the agent name from the call frame
                when the agent is first run.
            model_settings: Optional model request settings to use for this agent's runs, by default.
            retries: The default number of retries to allow before raising an error.
            result_tool_name: The name of the tool to use for the final result.
            result_tool_description: The description of the final result tool.
            result_retries: The maximum number of retries to allow for result validation, defaults to `retries`.
            tools: Tools to register with the agent, you can also register tools via the decorators
                [`@agent.tool`][pydantic_ai.Agent.tool] and [`@agent.tool_plain`][pydantic_ai.Agent.tool_plain].
            defer_model_check: by default, if you provide a [named][pydantic_ai.models.KnownModelName] model,
                it's evaluated to create a [`Model`][pydantic_ai.models.Model] instance immediately,
                which checks for the necessary environment variables. Set this to `false`
                to defer the evaluation until the first run. Useful if you want to
                [override the model][pydantic_ai.Agent.override] for testing.
            end_strategy: Strategy for handling tool calls that are requested alongside a final result.
                See [`EndStrategy`][pydantic_ai.agent.EndStrategy] for more information.
            instrument: Set to True to automatically instrument with OpenTelemetry,
                which will use Logfire if it's configured.
                Set to an instance of [`InstrumentationSettings`][pydantic_ai.agent.InstrumentationSettings] to customize.
                If this isn't set, then the last value set by
                [`Agent.instrument_all()`][pydantic_ai.Agent.instrument_all]
                will be used, which defaults to False.
        """
        if model is None or defer_model_check:
            self.model = model
        else:
            self.model = models.infer_model(model)

        self.end_strategy = end_strategy
        self.name = name
        self.model_settings = model_settings
        self.result_type = result_type
        self.instrument = instrument

        self._deps_type = deps_type

        self._result_tool_name = result_tool_name
        self._result_tool_description = result_tool_description
        self._result_schema: _result.ResultSchema[ResultDataT] | None = _result.ResultSchema[result_type].build(
            result_type, result_tool_name, result_tool_description
        )
        self._result_validators: list[_result.ResultValidator[AgentDepsT, ResultDataT]] = []

        self._system_prompts = (system_prompt,) if isinstance(system_prompt, str) else tuple(system_prompt)
        self._system_prompt_functions: list[_system_prompt.SystemPromptRunner[AgentDepsT]] = []
        self._system_prompt_dynamic_functions: dict[str, _system_prompt.SystemPromptRunner[AgentDepsT]] = {}

        self._function_tools: dict[str, Tool[AgentDepsT]] = {}

        self._default_retries = retries
        self._max_result_retries = result_retries if result_retries is not None else retries
        for tool in tools:
            if isinstance(tool, Tool):
                self._register_tool(tool)
            else:
                self._register_tool(Tool(tool))

    @staticmethod
    def instrument_all(instrument: InstrumentationSettings | bool = True) -> None:
        """Set the instrumentation options for all agents where `instrument` is not set."""
        Agent._instrument_default = instrument

    @overload
    async def run(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[ResultDataT]: ...

    @overload
    async def run(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT],
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[RunResultDataT]: ...

    async def run(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[Any]:
        """Run the agent with a user prompt in async mode.

        This method builds an internal agent graph (using system prompts, tools and result schemas) and then
        runs the graph to completion. The result of the run is returned.

        Example:
        ```python
        from pydantic_ai import Agent

        agent = Agent('openai:gpt-4o')

        async def main():
            agent_run = await agent.run('What is the capital of France?')
            print(agent_run.data)
            #> Paris
        ```

        Args:
            user_prompt: User input to start/continue the conversation.
            result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
                result validators since result validators would expect an argument that matches the agent's result type.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.

        Returns:
            The result of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        async with self.iter(
            user_prompt=user_prompt,
            result_type=result_type,
            message_history=message_history,
            model=model,
            deps=deps,
            model_settings=model_settings,
            usage_limits=usage_limits,
            usage=usage,
        ) as agent_run:
            async for _ in agent_run:
                pass

        assert (final_result := agent_run.result) is not None, 'The graph run did not finish properly'
        return final_result

    @asynccontextmanager
    async def iter(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AsyncIterator[AgentRun[AgentDepsT, Any]]:
        """A contextmanager which can be used to iterate over the agent graph's nodes as they are executed.

        This method builds an internal agent graph (using system prompts, tools and result schemas) and then returns an
        `AgentRun` object. The `AgentRun` can be used to async-iterate over the nodes of the graph as they are
        executed. This is the API to use if you want to consume the outputs coming from each LLM model response, or the
        stream of events coming from the execution of tools.

        The `AgentRun` also provides methods to access the full message history, new messages, and usage statistics,
        and the final result of the run once it has completed.

        For more details, see the documentation of `AgentRun`.

        Example:
        ```python
        from pydantic_ai import Agent

        agent = Agent('openai:gpt-4o')

        async def main():
            nodes = []
            async with agent.iter('What is the capital of France?') as agent_run:
                async for node in agent_run:
                    nodes.append(node)
            print(nodes)
            '''
            [
                ModelRequestNode(
                    request=ModelRequest(
                        parts=[
                            UserPromptPart(
                                content='What is the capital of France?',
                                timestamp=datetime.datetime(...),
                                part_kind='user-prompt',
                            )
                        ],
                        kind='request',
                    )
                ),
                CallToolsNode(
                    model_response=ModelResponse(
                        parts=[TextPart(content='Paris', part_kind='text')],
                        model_name='gpt-4o',
                        timestamp=datetime.datetime(...),
                        kind='response',
                    )
                ),
                End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
            ]
            '''
            print(agent_run.result.data)
            #> Paris
        ```

        Args:
            user_prompt: User input to start/continue the conversation.
            result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
                result validators since result validators would expect an argument that matches the agent's result type.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.

        Returns:
            The result of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        model_used = self._get_model(model)
        del model

        deps = self._get_deps(deps)
        new_message_index = len(message_history) if message_history else 0
        result_schema: _result.ResultSchema[RunResultDataT] | None = self._prepare_result_schema(result_type)

        # Build the graph
        graph = self._build_graph(result_type)

        # Build the initial state
        state = _agent_graph.GraphAgentState(
            message_history=message_history[:] if message_history else [],
            usage=usage or _usage.Usage(),
            retries=0,
            run_step=0,
        )

        # We consider it a user error if a user tries to restrict the result type while having a result validator that
        # may change the result type from the restricted type to something else. Therefore, we consider the following
        # typecast reasonable, even though it is possible to violate it with otherwise-type-checked code.
        result_validators = cast(list[_result.ResultValidator[AgentDepsT, RunResultDataT]], self._result_validators)

        # TODO: Instead of this, copy the function tools to ensure they don't share current_retry state between agent
        #  runs. Requires some changes to `Tool` to make them copyable though.
        for v in self._function_tools.values():
            v.current_retry = 0

        model_settings = merge_model_settings(self.model_settings, model_settings)
        usage_limits = usage_limits or _usage.UsageLimits()

        if isinstance(model_used, InstrumentedModel):
            tracer = model_used.options.tracer
        else:
            tracer = NoOpTracer()
        agent_name = self.name or 'agent'
        run_span = tracer.start_span(
            'agent run',
            attributes={
                'model_name': model_used.model_name if model_used else 'no-model',
                'agent_name': agent_name,
                'logfire.msg': f'{agent_name} run',
            },
        )

        graph_deps = _agent_graph.GraphAgentDeps[AgentDepsT, RunResultDataT](
            user_deps=deps,
            prompt=user_prompt,
            new_message_index=new_message_index,
            model=model_used,
            model_settings=model_settings,
            usage_limits=usage_limits,
            max_result_retries=self._max_result_retries,
            end_strategy=self.end_strategy,
            result_schema=result_schema,
            result_tools=self._result_schema.tool_defs() if self._result_schema else [],
            result_validators=result_validators,
            function_tools=self._function_tools,
            run_span=run_span,
            tracer=tracer,
        )
        start_node = _agent_graph.UserPromptNode[AgentDepsT](
            user_prompt=user_prompt,
            system_prompts=self._system_prompts,
            system_prompt_functions=self._system_prompt_functions,
            system_prompt_dynamic_functions=self._system_prompt_dynamic_functions,
        )

        async with graph.iter(
            start_node,
            state=state,
            deps=graph_deps,
            infer_name=False,
            span=use_span(run_span, end_on_exit=True),
        ) as graph_run:
            yield AgentRun(graph_run)

    @overload
    def run_sync(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[ResultDataT]: ...

    @overload
    def run_sync(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[RunResultDataT]: ...

    def run_sync(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[Any]:
        """Synchronously run the agent with a user prompt.

        This is a convenience method that wraps [`self.run`][pydantic_ai.Agent.run] with `loop.run_until_complete(...)`.
        You therefore can't use this method inside async code or if there's an active event loop.

        Example:
        ```python
        from pydantic_ai import Agent

        agent = Agent('openai:gpt-4o')

        result_sync = agent.run_sync('What is the capital of Italy?')
        print(result_sync.data)
        #> Rome
        ```

        Args:
            user_prompt: User input to start/continue the conversation.
            result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
                result validators since result validators would expect an argument that matches the agent's result type.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.

        Returns:
            The result of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        return get_event_loop().run_until_complete(
            self.run(
                user_prompt,
                result_type=result_type,
                message_history=message_history,
                model=model,
                deps=deps,
                model_settings=model_settings,
                usage_limits=usage_limits,
                usage=usage,
                infer_name=False,
            )
        )

    @overload
    def run_stream(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AbstractAsyncContextManager[result.StreamedRunResult[AgentDepsT, ResultDataT]]: ...

    @overload
    def run_stream(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT],
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AbstractAsyncContextManager[result.StreamedRunResult[AgentDepsT, RunResultDataT]]: ...

    @asynccontextmanager
    async def run_stream(  # noqa C901
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AsyncIterator[result.StreamedRunResult[AgentDepsT, Any]]:
        """Run the agent with a user prompt in async mode, returning a streamed response.

        Example:
        ```python
        from pydantic_ai import Agent

        agent = Agent('openai:gpt-4o')

        async def main():
            async with agent.run_stream('What is the capital of the UK?') as response:
                print(await response.get_data())
                #> London
        ```

        Args:
            user_prompt: User input to start/continue the conversation.
            result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
                result validators since result validators would expect an argument that matches the agent's result type.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.

        Returns:
            The result of the run.
        """
        # TODO: We need to deprecate this now that we have the `iter` method.
        #   Before that, though, we should add an event for when we reach the final result of the stream.
        if infer_name and self.name is None:
            # f_back because `asynccontextmanager` adds one frame
            if frame := inspect.currentframe():  # pragma: no branch
                self._infer_name(frame.f_back)

        yielded = False
        async with self.iter(
            user_prompt,
            result_type=result_type,
            message_history=message_history,
            model=model,
            deps=deps,
            model_settings=model_settings,
            usage_limits=usage_limits,
            usage=usage,
            infer_name=False,
        ) as agent_run:
            first_node = agent_run.next_node  # start with the first node
            assert isinstance(first_node, _agent_graph.UserPromptNode)  # the first node should be a user prompt node
            node = first_node
            while True:
                if self.is_model_request_node(node):
                    graph_ctx = agent_run.ctx
                    async with node._stream(graph_ctx) as streamed_response:  # pyright: ignore[reportPrivateUsage]

                        async def stream_to_final(
                            s: models.StreamedResponse,
                        ) -> FinalResult[models.StreamedResponse] | None:
                            result_schema = graph_ctx.deps.result_schema
                            async for maybe_part_event in streamed_response:
                                if isinstance(maybe_part_event, _messages.PartStartEvent):
                                    new_part = maybe_part_event.part
                                    if isinstance(new_part, _messages.TextPart):
                                        if _agent_graph.allow_text_result(result_schema):
                                            return FinalResult(s, None, None)
                                    elif isinstance(new_part, _messages.ToolCallPart) and result_schema:
                                        for call, _ in result_schema.find_tool([new_part]):
                                            return FinalResult(s, call.tool_name, call.tool_call_id)
                            return None

                        final_result_details = await stream_to_final(streamed_response)
                        if final_result_details is not None:
                            if yielded:
                                raise exceptions.AgentRunError('Agent run produced final results')
                            yielded = True

                            messages = graph_ctx.state.message_history.copy()

                            async def on_complete() -> None:
                                """Called when the stream has completed.

                                The model response will have been added to messages by now
                                by `StreamedRunResult._marked_completed`.
                                """
                                last_message = messages[-1]
                                assert isinstance(last_message, _messages.ModelResponse)
                                tool_calls = [
                                    part for part in last_message.parts if isinstance(part, _messages.ToolCallPart)
                                ]

                                parts: list[_messages.ModelRequestPart] = []
                                async for _event in _agent_graph.process_function_tools(
                                    tool_calls,
                                    final_result_details.tool_name,
                                    final_result_details.tool_call_id,
                                    graph_ctx,
                                    parts,
                                ):
                                    pass
                                # TODO: Should we do something here related to the retry count?
                                #   Maybe we should move the incrementing of the retry count to where we actually make a request?
                                # if any(isinstance(part, _messages.RetryPromptPart) for part in parts):
                                #     ctx.state.increment_retries(ctx.deps.max_result_retries)
                                if parts:
                                    messages.append(_messages.ModelRequest(parts))

                            yield StreamedRunResult(
                                messages,
                                graph_ctx.deps.new_message_index,
                                graph_ctx.deps.usage_limits,
                                streamed_response,
                                graph_ctx.deps.result_schema,
                                _agent_graph.build_run_context(graph_ctx),
                                graph_ctx.deps.result_validators,
                                final_result_details.tool_name,
                                on_complete,
                            )
                            break
                next_node = await agent_run.next(node)
                if not isinstance(next_node, _agent_graph.AgentNode):
                    raise exceptions.AgentRunError('Should have produced a StreamedRunResult before getting here')
                node = cast(_agent_graph.AgentNode[Any, Any], next_node)

        if not yielded:
            raise exceptions.AgentRunError('Agent run finished without producing a final result')

    @contextmanager
    def override(
        self,
        *,
        deps: AgentDepsT | _utils.Unset = _utils.UNSET,
        model: models.Model | models.KnownModelName | _utils.Unset = _utils.UNSET,
    ) -> Iterator[None]:
        """Context manager to temporarily override agent dependencies and model.

        This is particularly useful when testing.
        You can find an example of this [here](../testing-evals.md#overriding-model-via-pytest-fixtures).

        Args:
            deps: The dependencies to use instead of the dependencies passed to the agent run.
            model: The model to use instead of the model passed to the agent run.
        """
        if _utils.is_set(deps):
            override_deps_before = self._override_deps
            self._override_deps = _utils.Some(deps)
        else:
            override_deps_before = _utils.UNSET

        # noinspection PyTypeChecker
        if _utils.is_set(model):
            override_model_before = self._override_model
            # noinspection PyTypeChecker
            self._override_model = _utils.Some(models.infer_model(model))  # pyright: ignore[reportArgumentType]
        else:
            override_model_before = _utils.UNSET

        try:
            yield
        finally:
            if _utils.is_set(override_deps_before):
                self._override_deps = override_deps_before
            if _utils.is_set(override_model_before):
                self._override_model = override_model_before

    @overload
    def system_prompt(
        self, func: Callable[[RunContext[AgentDepsT]], str], /
    ) -> Callable[[RunContext[AgentDepsT]], str]: ...

    @overload
    def system_prompt(
        self, func: Callable[[RunContext[AgentDepsT]], Awaitable[str]], /
    ) -> Callable[[RunContext[AgentDepsT]], Awaitable[str]]: ...

    @overload
    def system_prompt(self, func: Callable[[], str], /) -> Callable[[], str]: ...

    @overload
    def system_prompt(self, func: Callable[[], Awaitable[str]], /) -> Callable[[], Awaitable[str]]: ...

    @overload
    def system_prompt(
        self, /, *, dynamic: bool = False
    ) -> Callable[[_system_prompt.SystemPromptFunc[AgentDepsT]], _system_prompt.SystemPromptFunc[AgentDepsT]]: ...

    def system_prompt(
        self,
        func: _system_prompt.SystemPromptFunc[AgentDepsT] | None = None,
        /,
        *,
        dynamic: bool = False,
    ) -> (
        Callable[[_system_prompt.SystemPromptFunc[AgentDepsT]], _system_prompt.SystemPromptFunc[AgentDepsT]]
        | _system_prompt.SystemPromptFunc[AgentDepsT]
    ):
        """Decorator to register a system prompt function.

        Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its only argument.
        Can decorate a sync or async functions.

        The decorator can be used either bare (`agent.system_prompt`) or as a function call
        (`agent.system_prompt(...)`), see the examples below.

        Overloads for every possible signature of `system_prompt` are included so the decorator doesn't obscure
        the type of the function, see `tests/typed_agent.py` for tests.

        Args:
            func: The function to decorate
            dynamic: If True, the system prompt will be reevaluated even when `messages_history` is provided,
                see [`SystemPromptPart.dynamic_ref`][pydantic_ai.messages.SystemPromptPart.dynamic_ref]

        Example:
        ```python
        from pydantic_ai import Agent, RunContext

        agent = Agent('test', deps_type=str)

        @agent.system_prompt
        def simple_system_prompt() -> str:
            return 'foobar'

        @agent.system_prompt(dynamic=True)
        async def async_system_prompt(ctx: RunContext[str]) -> str:
            return f'{ctx.deps} is the best'
        ```
        """
        if func is None:

            def decorator(
                func_: _system_prompt.SystemPromptFunc[AgentDepsT],
            ) -> _system_prompt.SystemPromptFunc[AgentDepsT]:
                runner = _system_prompt.SystemPromptRunner[AgentDepsT](func_, dynamic=dynamic)
                self._system_prompt_functions.append(runner)
                if dynamic:
                    self._system_prompt_dynamic_functions[func_.__qualname__] = runner
                return func_

            return decorator
        else:
            assert not dynamic, "dynamic can't be True in this case"
            self._system_prompt_functions.append(_system_prompt.SystemPromptRunner[AgentDepsT](func, dynamic=dynamic))
            return func

    @overload
    def result_validator(
        self, func: Callable[[RunContext[AgentDepsT], ResultDataT], ResultDataT], /
    ) -> Callable[[RunContext[AgentDepsT], ResultDataT], ResultDataT]: ...

    @overload
    def result_validator(
        self, func: Callable[[RunContext[AgentDepsT], ResultDataT], Awaitable[ResultDataT]], /
    ) -> Callable[[RunContext[AgentDepsT], ResultDataT], Awaitable[ResultDataT]]: ...

    @overload
    def result_validator(
        self, func: Callable[[ResultDataT], ResultDataT], /
    ) -> Callable[[ResultDataT], ResultDataT]: ...

    @overload
    def result_validator(
        self, func: Callable[[ResultDataT], Awaitable[ResultDataT]], /
    ) -> Callable[[ResultDataT], Awaitable[ResultDataT]]: ...

    def result_validator(
        self, func: _result.ResultValidatorFunc[AgentDepsT, ResultDataT], /
    ) -> _result.ResultValidatorFunc[AgentDepsT, ResultDataT]:
        """Decorator to register a result validator function.

        Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.
        Can decorate a sync or async functions.

        Overloads for every possible signature of `result_validator` are included so the decorator doesn't obscure
        the type of the function, see `tests/typed_agent.py` for tests.

        Example:
        ```python
        from pydantic_ai import Agent, ModelRetry, RunContext

        agent = Agent('test', deps_type=str)

        @agent.result_validator
        def result_validator_simple(data: str) -> str:
            if 'wrong' in data:
                raise ModelRetry('wrong response')
            return data

        @agent.result_validator
        async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
            if ctx.deps in data:
                raise ModelRetry('wrong response')
            return data

        result = agent.run_sync('foobar', deps='spam')
        print(result.data)
        #> success (no tool calls)
        ```
        """
        self._result_validators.append(_result.ResultValidator[AgentDepsT, Any](func))
        return func

    @overload
    def tool(self, func: ToolFuncContext[AgentDepsT, ToolParams], /) -> ToolFuncContext[AgentDepsT, ToolParams]: ...

    @overload
    def tool(
        self,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ) -> Callable[[ToolFuncContext[AgentDepsT, ToolParams]], ToolFuncContext[AgentDepsT, ToolParams]]: ...

    def tool(
        self,
        func: ToolFuncContext[AgentDepsT, ToolParams] | None = None,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ) -> Any:
        """Decorator to register a tool function which takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.

        Can decorate a sync or async functions.

        The docstring is inspected to extract both the tool description and description of each parameter,
        [learn more](../tools.md#function-tools-and-schema).

        We can't add overloads for every possible signature of tool, since the return type is a recursive union
        so the signature of functions decorated with `@agent.tool` is obscured.

        Example:
        ```python
        from pydantic_ai import Agent, RunContext

        agent = Agent('test', deps_type=int)

        @agent.tool
        def foobar(ctx: RunContext[int], x: int) -> int:
            return ctx.deps + x

        @agent.tool(retries=2)
        async def spam(ctx: RunContext[str], y: float) -> float:
            return ctx.deps + y

        result = agent.run_sync('foobar', deps=1)
        print(result.data)
        #> {"foobar":1,"spam":1.0}
        ```

        Args:
            func: The tool function to register.
            retries: The number of retries to allow for this tool, defaults to the agent's default retries,
                which defaults to 1.
            prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                tool from a given step. This is useful if you want to customise a tool at call time,
                or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
            docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
                Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
            require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
        """
        if func is None:

            def tool_decorator(
                func_: ToolFuncContext[AgentDepsT, ToolParams],
            ) -> ToolFuncContext[AgentDepsT, ToolParams]:
                # noinspection PyTypeChecker
                self._register_function(func_, True, retries, prepare, docstring_format, require_parameter_descriptions)
                return func_

            return tool_decorator
        else:
            # noinspection PyTypeChecker
            self._register_function(func, True, retries, prepare, docstring_format, require_parameter_descriptions)
            return func

    @overload
    def tool_plain(self, func: ToolFuncPlain[ToolParams], /) -> ToolFuncPlain[ToolParams]: ...

    @overload
    def tool_plain(
        self,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ) -> Callable[[ToolFuncPlain[ToolParams]], ToolFuncPlain[ToolParams]]: ...

    def tool_plain(
        self,
        func: ToolFuncPlain[ToolParams] | None = None,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ) -> Any:
        """Decorator to register a tool function which DOES NOT take `RunContext` as an argument.

        Can decorate a sync or async functions.

        The docstring is inspected to extract both the tool description and description of each parameter,
        [learn more](../tools.md#function-tools-and-schema).

        We can't add overloads for every possible signature of tool, since the return type is a recursive union
        so the signature of functions decorated with `@agent.tool` is obscured.

        Example:
        ```python
        from pydantic_ai import Agent, RunContext

        agent = Agent('test')

        @agent.tool
        def foobar(ctx: RunContext[int]) -> int:
            return 123

        @agent.tool(retries=2)
        async def spam(ctx: RunContext[str]) -> float:
            return 3.14

        result = agent.run_sync('foobar', deps=1)
        print(result.data)
        #> {"foobar":123,"spam":3.14}
        ```

        Args:
            func: The tool function to register.
            retries: The number of retries to allow for this tool, defaults to the agent's default retries,
                which defaults to 1.
            prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                tool from a given step. This is useful if you want to customise a tool at call time,
                or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
            docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
                Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
            require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
        """
        if func is None:

            def tool_decorator(func_: ToolFuncPlain[ToolParams]) -> ToolFuncPlain[ToolParams]:
                # noinspection PyTypeChecker
                self._register_function(
                    func_, False, retries, prepare, docstring_format, require_parameter_descriptions
                )
                return func_

            return tool_decorator
        else:
            self._register_function(func, False, retries, prepare, docstring_format, require_parameter_descriptions)
            return func

    def _register_function(
        self,
        func: ToolFuncEither[AgentDepsT, ToolParams],
        takes_ctx: bool,
        retries: int | None,
        prepare: ToolPrepareFunc[AgentDepsT] | None,
        docstring_format: DocstringFormat,
        require_parameter_descriptions: bool,
    ) -> None:
        """Private utility to register a function as a tool."""
        retries_ = retries if retries is not None else self._default_retries
        tool = Tool[AgentDepsT](
            func,
            takes_ctx=takes_ctx,
            max_retries=retries_,
            prepare=prepare,
            docstring_format=docstring_format,
            require_parameter_descriptions=require_parameter_descriptions,
        )
        self._register_tool(tool)

    def _register_tool(self, tool: Tool[AgentDepsT]) -> None:
        """Private utility to register a tool instance."""
        if tool.max_retries is None:
            # noinspection PyTypeChecker
            tool = dataclasses.replace(tool, max_retries=self._default_retries)

        if tool.name in self._function_tools:
            raise exceptions.UserError(f'Tool name conflicts with existing tool: {tool.name!r}')

        if self._result_schema and tool.name in self._result_schema.tools:
            raise exceptions.UserError(f'Tool name conflicts with result schema name: {tool.name!r}')

        self._function_tools[tool.name] = tool

    def _get_model(self, model: models.Model | models.KnownModelName | None) -> models.Model:
        """Create a model configured for this agent.

        Args:
            model: model to use for this run, required if `model` was not set when creating the agent.

        Returns:
            The model used
        """
        model_: models.Model
        if some_model := self._override_model:
            # we don't want `override()` to cover up errors from the model not being defined, hence this check
            if model is None and self.model is None:
                raise exceptions.UserError(
                    '`model` must be set either when creating the agent or when calling it. '
                    '(Even when `override(model=...)` is customizing the model that will actually be called)'
                )
            model_ = some_model.value
        elif model is not None:
            model_ = models.infer_model(model)
        elif self.model is not None:
            # noinspection PyTypeChecker
            model_ = self.model = models.infer_model(self.model)
        else:
            raise exceptions.UserError('`model` must be set either when creating the agent or when calling it.')

        instrument = self.instrument
        if instrument is None:
            instrument = self._instrument_default

        if instrument and not isinstance(model_, InstrumentedModel):
            if instrument is True:
                instrument = InstrumentationSettings()

            model_ = InstrumentedModel(model_, instrument)

        return model_

    def _get_deps(self: Agent[T, ResultDataT], deps: T) -> T:
        """Get deps for a run.

        If we've overridden deps via `_override_deps`, use that, otherwise use the deps passed to the call.

        We could do runtime type checking of deps against `self._deps_type`, but that's a slippery slope.
        """
        if some_deps := self._override_deps:
            return some_deps.value
        else:
            return deps

    def _infer_name(self, function_frame: FrameType | None) -> None:
        """Infer the agent name from the call frame.

        Usage should be `self._infer_name(inspect.currentframe())`.
        """
        assert self.name is None, 'Name already set'
        if function_frame is not None:  # pragma: no branch
            if parent_frame := function_frame.f_back:  # pragma: no branch
                for name, item in parent_frame.f_locals.items():
                    if item is self:
                        self.name = name
                        return
                if parent_frame.f_locals != parent_frame.f_globals:
                    # if we couldn't find the agent in locals and globals are a different dict, try globals
                    for name, item in parent_frame.f_globals.items():
                        if item is self:
                            self.name = name
                            return

    @property
    @deprecated(
        'The `last_run_messages` attribute has been removed, use `capture_run_messages` instead.', category=None
    )
    def last_run_messages(self) -> list[_messages.ModelMessage]:
        raise AttributeError('The `last_run_messages` attribute has been removed, use `capture_run_messages` instead.')

    def _build_graph(
        self, result_type: type[RunResultDataT] | None
    ) -> Graph[_agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any], FinalResult[Any]]:
        return _agent_graph.build_agent_graph(self.name, self._deps_type, result_type or self.result_type)

    def _prepare_result_schema(
        self, result_type: type[RunResultDataT] | None
    ) -> _result.ResultSchema[RunResultDataT] | None:
        if result_type is not None:
            if self._result_validators:
                raise exceptions.UserError('Cannot set a custom run `result_type` when the agent has result validators')
            return _result.ResultSchema[result_type].build(
                result_type, self._result_tool_name, self._result_tool_description
            )
        else:
            return self._result_schema  # pyright: ignore[reportReturnType]

    @staticmethod
    def is_model_request_node(
        node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
    ) -> TypeGuard[_agent_graph.ModelRequestNode[T, S]]:
        """Check if the node is a `ModelRequestNode`, narrowing the type if it is.

        This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
        """
        return isinstance(node, _agent_graph.ModelRequestNode)

    @staticmethod
    def is_call_tools_node(
        node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
    ) -> TypeGuard[_agent_graph.CallToolsNode[T, S]]:
        """Check if the node is a `CallToolsNode`, narrowing the type if it is.

        This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
        """
        return isinstance(node, _agent_graph.CallToolsNode)

    @staticmethod
    def is_user_prompt_node(
        node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
    ) -> TypeGuard[_agent_graph.UserPromptNode[T, S]]:
        """Check if the node is a `UserPromptNode`, narrowing the type if it is.

        This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
        """
        return isinstance(node, _agent_graph.UserPromptNode)

    @staticmethod
    def is_end_node(
        node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
    ) -> TypeGuard[End[result.FinalResult[S]]]:
        """Check if the node is a `End`, narrowing the type if it is.

        This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
        """
        return isinstance(node, End)
```

```
@final
@dataclasses.dataclass(init=False)
class Agent(Generic[AgentDepsT, ResultDataT]):
    """Class for defining "agents" - a way to have a specific type of "conversation" with an LLM.

    Agents are generic in the dependency type they take [`AgentDepsT`][pydantic_ai.tools.AgentDepsT]
    and the result data type they return, [`ResultDataT`][pydantic_ai.result.ResultDataT].

    By default, if neither generic parameter is customised, agents have type `Agent[None, str]`.

    Minimal usage example:

    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')
    result = agent.run_sync('What is the capital of France?')
    print(result.data)
    #> Paris
    ```
    """

    # we use dataclass fields in order to conveniently know what attributes are available
    model: models.Model | models.KnownModelName | None
    """The default model configured for this agent."""

    name: str | None
    """The name of the agent, used for logging.

    If `None`, we try to infer the agent name from the call frame when the agent is first run.
    """
    end_strategy: EndStrategy
    """Strategy for handling tool calls when a final result is found."""

    model_settings: ModelSettings | None
    """Optional model request settings to use for this agents's runs, by default.

    Note, if `model_settings` is provided by `run`, `run_sync`, or `run_stream`, those settings will
    be merged with this value, with the runtime argument taking priority.
    """

    result_type: type[ResultDataT] = dataclasses.field(repr=False)
    """
    The type of the result data, used to validate the result data, defaults to `str`.
    """

    instrument: InstrumentationSettings | bool | None
    """Options to automatically instrument with OpenTelemetry."""

    _instrument_default: ClassVar[InstrumentationSettings | bool] = False

    _deps_type: type[AgentDepsT] = dataclasses.field(repr=False)
    _result_tool_name: str = dataclasses.field(repr=False)
    _result_tool_description: str | None = dataclasses.field(repr=False)
    _result_schema: _result.ResultSchema[ResultDataT] | None = dataclasses.field(repr=False)
    _result_validators: list[_result.ResultValidator[AgentDepsT, ResultDataT]] = dataclasses.field(repr=False)
    _system_prompts: tuple[str, ...] = dataclasses.field(repr=False)
    _system_prompt_functions: list[_system_prompt.SystemPromptRunner[AgentDepsT]] = dataclasses.field(repr=False)
    _system_prompt_dynamic_functions: dict[str, _system_prompt.SystemPromptRunner[AgentDepsT]] = dataclasses.field(
        repr=False
    )
    _function_tools: dict[str, Tool[AgentDepsT]] = dataclasses.field(repr=False)
    _default_retries: int = dataclasses.field(repr=False)
    _max_result_retries: int = dataclasses.field(repr=False)
    _override_deps: _utils.Option[AgentDepsT] = dataclasses.field(default=None, repr=False)
    _override_model: _utils.Option[models.Model] = dataclasses.field(default=None, repr=False)

    def __init__(
        self,
        model: models.Model | models.KnownModelName | None = None,
        *,
        result_type: type[ResultDataT] = str,
        system_prompt: str | Sequence[str] = (),
        deps_type: type[AgentDepsT] = NoneType,
        name: str | None = None,
        model_settings: ModelSettings | None = None,
        retries: int = 1,
        result_tool_name: str = 'final_result',
        result_tool_description: str | None = None,
        result_retries: int | None = None,
        tools: Sequence[Tool[AgentDepsT] | ToolFuncEither[AgentDepsT, ...]] = (),
        defer_model_check: bool = False,
        end_strategy: EndStrategy = 'early',
        instrument: InstrumentationSettings | bool | None = None,
    ):
        """Create an agent.

        Args:
            model: The default model to use for this agent, if not provide,
                you must provide the model when calling it.
            result_type: The type of the result data, used to validate the result data, defaults to `str`.
            system_prompt: Static system prompts to use for this agent, you can also register system
                prompts via a function with [`system_prompt`][pydantic_ai.Agent.system_prompt].
            deps_type: The type used for dependency injection, this parameter exists solely to allow you to fully
                parameterize the agent, and therefore get the best out of static type checking.
                If you're not using deps, but want type checking to pass, you can set `deps=None` to satisfy Pyright
                or add a type hint `: Agent[None, <return type>]`.
            name: The name of the agent, used for logging. If `None`, we try to infer the agent name from the call frame
                when the agent is first run.
            model_settings: Optional model request settings to use for this agent's runs, by default.
            retries: The default number of retries to allow before raising an error.
            result_tool_name: The name of the tool to use for the final result.
            result_tool_description: The description of the final result tool.
            result_retries: The maximum number of retries to allow for result validation, defaults to `retries`.
            tools: Tools to register with the agent, you can also register tools via the decorators
                [`@agent.tool`][pydantic_ai.Agent.tool] and [`@agent.tool_plain`][pydantic_ai.Agent.tool_plain].
            defer_model_check: by default, if you provide a [named][pydantic_ai.models.KnownModelName] model,
                it's evaluated to create a [`Model`][pydantic_ai.models.Model] instance immediately,
                which checks for the necessary environment variables. Set this to `false`
                to defer the evaluation until the first run. Useful if you want to
                [override the model][pydantic_ai.Agent.override] for testing.
            end_strategy: Strategy for handling tool calls that are requested alongside a final result.
                See [`EndStrategy`][pydantic_ai.agent.EndStrategy] for more information.
            instrument: Set to True to automatically instrument with OpenTelemetry,
                which will use Logfire if it's configured.
                Set to an instance of [`InstrumentationSettings`][pydantic_ai.agent.InstrumentationSettings] to customize.
                If this isn't set, then the last value set by
                [`Agent.instrument_all()`][pydantic_ai.Agent.instrument_all]
                will be used, which defaults to False.
        """
        if model is None or defer_model_check:
            self.model = model
        else:
            self.model = models.infer_model(model)

        self.end_strategy = end_strategy
        self.name = name
        self.model_settings = model_settings
        self.result_type = result_type
        self.instrument = instrument

        self._deps_type = deps_type

        self._result_tool_name = result_tool_name
        self._result_tool_description = result_tool_description
        self._result_schema: _result.ResultSchema[ResultDataT] | None = _result.ResultSchema[result_type].build(
            result_type, result_tool_name, result_tool_description
        )
        self._result_validators: list[_result.ResultValidator[AgentDepsT, ResultDataT]] = []

        self._system_prompts = (system_prompt,) if isinstance(system_prompt, str) else tuple(system_prompt)
        self._system_prompt_functions: list[_system_prompt.SystemPromptRunner[AgentDepsT]] = []
        self._system_prompt_dynamic_functions: dict[str, _system_prompt.SystemPromptRunner[AgentDepsT]] = {}

        self._function_tools: dict[str, Tool[AgentDepsT]] = {}

        self._default_retries = retries
        self._max_result_retries = result_retries if result_retries is not None else retries
        for tool in tools:
            if isinstance(tool, Tool):
                self._register_tool(tool)
            else:
                self._register_tool(Tool(tool))

    @staticmethod
    def instrument_all(instrument: InstrumentationSettings | bool = True) -> None:
        """Set the instrumentation options for all agents where `instrument` is not set."""
        Agent._instrument_default = instrument

    @overload
    async def run(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[ResultDataT]: ...

    @overload
    async def run(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT],
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[RunResultDataT]: ...

    async def run(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[Any]:
        """Run the agent with a user prompt in async mode.

        This method builds an internal agent graph (using system prompts, tools and result schemas) and then
        runs the graph to completion. The result of the run is returned.

        Example:
        ```python
        from pydantic_ai import Agent

        agent = Agent('openai:gpt-4o')

        async def main():
            agent_run = await agent.run('What is the capital of France?')
            print(agent_run.data)
            #> Paris
        ```

        Args:
            user_prompt: User input to start/continue the conversation.
            result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
                result validators since result validators would expect an argument that matches the agent's result type.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.

        Returns:
            The result of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        async with self.iter(
            user_prompt=user_prompt,
            result_type=result_type,
            message_history=message_history,
            model=model,
            deps=deps,
            model_settings=model_settings,
            usage_limits=usage_limits,
            usage=usage,
        ) as agent_run:
            async for _ in agent_run:
                pass

        assert (final_result := agent_run.result) is not None, 'The graph run did not finish properly'
        return final_result

    @asynccontextmanager
    async def iter(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AsyncIterator[AgentRun[AgentDepsT, Any]]:
        """A contextmanager which can be used to iterate over the agent graph's nodes as they are executed.

        This method builds an internal agent graph (using system prompts, tools and result schemas) and then returns an
        `AgentRun` object. The `AgentRun` can be used to async-iterate over the nodes of the graph as they are
        executed. This is the API to use if you want to consume the outputs coming from each LLM model response, or the
        stream of events coming from the execution of tools.

        The `AgentRun` also provides methods to access the full message history, new messages, and usage statistics,
        and the final result of the run once it has completed.

        For more details, see the documentation of `AgentRun`.

        Example:
        ```python
        from pydantic_ai import Agent

        agent = Agent('openai:gpt-4o')

        async def main():
            nodes = []
            async with agent.iter('What is the capital of France?') as agent_run:
                async for node in agent_run:
                    nodes.append(node)
            print(nodes)
            '''
            [
                ModelRequestNode(
                    request=ModelRequest(
                        parts=[
                            UserPromptPart(
                                content='What is the capital of France?',
                                timestamp=datetime.datetime(...),
                                part_kind='user-prompt',
                            )
                        ],
                        kind='request',
                    )
                ),
                CallToolsNode(
                    model_response=ModelResponse(
                        parts=[TextPart(content='Paris', part_kind='text')],
                        model_name='gpt-4o',
                        timestamp=datetime.datetime(...),
                        kind='response',
                    )
                ),
                End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
            ]
            '''
            print(agent_run.result.data)
            #> Paris
        ```

        Args:
            user_prompt: User input to start/continue the conversation.
            result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
                result validators since result validators would expect an argument that matches the agent's result type.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.

        Returns:
            The result of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        model_used = self._get_model(model)
        del model

        deps = self._get_deps(deps)
        new_message_index = len(message_history) if message_history else 0
        result_schema: _result.ResultSchema[RunResultDataT] | None = self._prepare_result_schema(result_type)

        # Build the graph
        graph = self._build_graph(result_type)

        # Build the initial state
        state = _agent_graph.GraphAgentState(
            message_history=message_history[:] if message_history else [],
            usage=usage or _usage.Usage(),
            retries=0,
            run_step=0,
        )

        # We consider it a user error if a user tries to restrict the result type while having a result validator that
        # may change the result type from the restricted type to something else. Therefore, we consider the following
        # typecast reasonable, even though it is possible to violate it with otherwise-type-checked code.
        result_validators = cast(list[_result.ResultValidator[AgentDepsT, RunResultDataT]], self._result_validators)

        # TODO: Instead of this, copy the function tools to ensure they don't share current_retry state between agent
        #  runs. Requires some changes to `Tool` to make them copyable though.
        for v in self._function_tools.values():
            v.current_retry = 0

        model_settings = merge_model_settings(self.model_settings, model_settings)
        usage_limits = usage_limits or _usage.UsageLimits()

        if isinstance(model_used, InstrumentedModel):
            tracer = model_used.options.tracer
        else:
            tracer = NoOpTracer()
        agent_name = self.name or 'agent'
        run_span = tracer.start_span(
            'agent run',
            attributes={
                'model_name': model_used.model_name if model_used else 'no-model',
                'agent_name': agent_name,
                'logfire.msg': f'{agent_name} run',
            },
        )

        graph_deps = _agent_graph.GraphAgentDeps[AgentDepsT, RunResultDataT](
            user_deps=deps,
            prompt=user_prompt,
            new_message_index=new_message_index,
            model=model_used,
            model_settings=model_settings,
            usage_limits=usage_limits,
            max_result_retries=self._max_result_retries,
            end_strategy=self.end_strategy,
            result_schema=result_schema,
            result_tools=self._result_schema.tool_defs() if self._result_schema else [],
            result_validators=result_validators,
            function_tools=self._function_tools,
            run_span=run_span,
            tracer=tracer,
        )
        start_node = _agent_graph.UserPromptNode[AgentDepsT](
            user_prompt=user_prompt,
            system_prompts=self._system_prompts,
            system_prompt_functions=self._system_prompt_functions,
            system_prompt_dynamic_functions=self._system_prompt_dynamic_functions,
        )

        async with graph.iter(
            start_node,
            state=state,
            deps=graph_deps,
            infer_name=False,
            span=use_span(run_span, end_on_exit=True),
        ) as graph_run:
            yield AgentRun(graph_run)

    @overload
    def run_sync(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[ResultDataT]: ...

    @overload
    def run_sync(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[RunResultDataT]: ...

    def run_sync(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AgentRunResult[Any]:
        """Synchronously run the agent with a user prompt.

        This is a convenience method that wraps [`self.run`][pydantic_ai.Agent.run] with `loop.run_until_complete(...)`.
        You therefore can't use this method inside async code or if there's an active event loop.

        Example:
        ```python
        from pydantic_ai import Agent

        agent = Agent('openai:gpt-4o')

        result_sync = agent.run_sync('What is the capital of Italy?')
        print(result_sync.data)
        #> Rome
        ```

        Args:
            user_prompt: User input to start/continue the conversation.
            result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
                result validators since result validators would expect an argument that matches the agent's result type.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.

        Returns:
            The result of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        return get_event_loop().run_until_complete(
            self.run(
                user_prompt,
                result_type=result_type,
                message_history=message_history,
                model=model,
                deps=deps,
                model_settings=model_settings,
                usage_limits=usage_limits,
                usage=usage,
                infer_name=False,
            )
        )

    @overload
    def run_stream(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AbstractAsyncContextManager[result.StreamedRunResult[AgentDepsT, ResultDataT]]: ...

    @overload
    def run_stream(
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT],
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AbstractAsyncContextManager[result.StreamedRunResult[AgentDepsT, RunResultDataT]]: ...

    @asynccontextmanager
    async def run_stream(  # noqa C901
        self,
        user_prompt: str | Sequence[_messages.UserContent],
        *,
        result_type: type[RunResultDataT] | None = None,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDepsT = None,
        model_settings: ModelSettings | None = None,
        usage_limits: _usage.UsageLimits | None = None,
        usage: _usage.Usage | None = None,
        infer_name: bool = True,
    ) -> AsyncIterator[result.StreamedRunResult[AgentDepsT, Any]]:
        """Run the agent with a user prompt in async mode, returning a streamed response.

        Example:
        ```python
        from pydantic_ai import Agent

        agent = Agent('openai:gpt-4o')

        async def main():
            async with agent.run_stream('What is the capital of the UK?') as response:
                print(await response.get_data())
                #> London
        ```

        Args:
            user_prompt: User input to start/continue the conversation.
            result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
                result validators since result validators would expect an argument that matches the agent's result type.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.

        Returns:
            The result of the run.
        """
        # TODO: We need to deprecate this now that we have the `iter` method.
        #   Before that, though, we should add an event for when we reach the final result of the stream.
        if infer_name and self.name is None:
            # f_back because `asynccontextmanager` adds one frame
            if frame := inspect.currentframe():  # pragma: no branch
                self._infer_name(frame.f_back)

        yielded = False
        async with self.iter(
            user_prompt,
            result_type=result_type,
            message_history=message_history,
            model=model,
            deps=deps,
            model_settings=model_settings,
            usage_limits=usage_limits,
            usage=usage,
            infer_name=False,
        ) as agent_run:
            first_node = agent_run.next_node  # start with the first node
            assert isinstance(first_node, _agent_graph.UserPromptNode)  # the first node should be a user prompt node
            node = first_node
            while True:
                if self.is_model_request_node(node):
                    graph_ctx = agent_run.ctx
                    async with node._stream(graph_ctx) as streamed_response:  # pyright: ignore[reportPrivateUsage]

                        async def stream_to_final(
                            s: models.StreamedResponse,
                        ) -> FinalResult[models.StreamedResponse] | None:
                            result_schema = graph_ctx.deps.result_schema
                            async for maybe_part_event in streamed_response:
                                if isinstance(maybe_part_event, _messages.PartStartEvent):
                                    new_part = maybe_part_event.part
                                    if isinstance(new_part, _messages.TextPart):
                                        if _agent_graph.allow_text_result(result_schema):
                                            return FinalResult(s, None, None)
                                    elif isinstance(new_part, _messages.ToolCallPart) and result_schema:
                                        for call, _ in result_schema.find_tool([new_part]):
                                            return FinalResult(s, call.tool_name, call.tool_call_id)
                            return None

                        final_result_details = await stream_to_final(streamed_response)
                        if final_result_details is not None:
                            if yielded:
                                raise exceptions.AgentRunError('Agent run produced final results')
                            yielded = True

                            messages = graph_ctx.state.message_history.copy()

                            async def on_complete() -> None:
                                """Called when the stream has completed.

                                The model response will have been added to messages by now
                                by `StreamedRunResult._marked_completed`.
                                """
                                last_message = messages[-1]
                                assert isinstance(last_message, _messages.ModelResponse)
                                tool_calls = [
                                    part for part in last_message.parts if isinstance(part, _messages.ToolCallPart)
                                ]

                                parts: list[_messages.ModelRequestPart] = []
                                async for _event in _agent_graph.process_function_tools(
                                    tool_calls,
                                    final_result_details.tool_name,
                                    final_result_details.tool_call_id,
                                    graph_ctx,
                                    parts,
                                ):
                                    pass
                                # TODO: Should we do something here related to the retry count?
                                #   Maybe we should move the incrementing of the retry count to where we actually make a request?
                                # if any(isinstance(part, _messages.RetryPromptPart) for part in parts):
                                #     ctx.state.increment_retries(ctx.deps.max_result_retries)
                                if parts:
                                    messages.append(_messages.ModelRequest(parts))

                            yield StreamedRunResult(
                                messages,
                                graph_ctx.deps.new_message_index,
                                graph_ctx.deps.usage_limits,
                                streamed_response,
                                graph_ctx.deps.result_schema,
                                _agent_graph.build_run_context(graph_ctx),
                                graph_ctx.deps.result_validators,
                                final_result_details.tool_name,
                                on_complete,
                            )
                            break
                next_node = await agent_run.next(node)
                if not isinstance(next_node, _agent_graph.AgentNode):
                    raise exceptions.AgentRunError('Should have produced a StreamedRunResult before getting here')
                node = cast(_agent_graph.AgentNode[Any, Any], next_node)

        if not yielded:
            raise exceptions.AgentRunError('Agent run finished without producing a final result')

    @contextmanager
    def override(
        self,
        *,
        deps: AgentDepsT | _utils.Unset = _utils.UNSET,
        model: models.Model | models.KnownModelName | _utils.Unset = _utils.UNSET,
    ) -> Iterator[None]:
        """Context manager to temporarily override agent dependencies and model.

        This is particularly useful when testing.
        You can find an example of this [here](../testing-evals.md#overriding-model-via-pytest-fixtures).

        Args:
            deps: The dependencies to use instead of the dependencies passed to the agent run.
            model: The model to use instead of the model passed to the agent run.
        """
        if _utils.is_set(deps):
            override_deps_before = self._override_deps
            self._override_deps = _utils.Some(deps)
        else:
            override_deps_before = _utils.UNSET

        # noinspection PyTypeChecker
        if _utils.is_set(model):
            override_model_before = self._override_model
            # noinspection PyTypeChecker
            self._override_model = _utils.Some(models.infer_model(model))  # pyright: ignore[reportArgumentType]
        else:
            override_model_before = _utils.UNSET

        try:
            yield
        finally:
            if _utils.is_set(override_deps_before):
                self._override_deps = override_deps_before
            if _utils.is_set(override_model_before):
                self._override_model = override_model_before

    @overload
    def system_prompt(
        self, func: Callable[[RunContext[AgentDepsT]], str], /
    ) -> Callable[[RunContext[AgentDepsT]], str]: ...

    @overload
    def system_prompt(
        self, func: Callable[[RunContext[AgentDepsT]], Awaitable[str]], /
    ) -> Callable[[RunContext[AgentDepsT]], Awaitable[str]]: ...

    @overload
    def system_prompt(self, func: Callable[[], str], /) -> Callable[[], str]: ...

    @overload
    def system_prompt(self, func: Callable[[], Awaitable[str]], /) -> Callable[[], Awaitable[str]]: ...

    @overload
    def system_prompt(
        self, /, *, dynamic: bool = False
    ) -> Callable[[_system_prompt.SystemPromptFunc[AgentDepsT]], _system_prompt.SystemPromptFunc[AgentDepsT]]: ...

    def system_prompt(
        self,
        func: _system_prompt.SystemPromptFunc[AgentDepsT] | None = None,
        /,
        *,
        dynamic: bool = False,
    ) -> (
        Callable[[_system_prompt.SystemPromptFunc[AgentDepsT]], _system_prompt.SystemPromptFunc[AgentDepsT]]
        | _system_prompt.SystemPromptFunc[AgentDepsT]
    ):
        """Decorator to register a system prompt function.

        Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its only argument.
        Can decorate a sync or async functions.

        The decorator can be used either bare (`agent.system_prompt`) or as a function call
        (`agent.system_prompt(...)`), see the examples below.

        Overloads for every possible signature of `system_prompt` are included so the decorator doesn't obscure
        the type of the function, see `tests/typed_agent.py` for tests.

        Args:
            func: The function to decorate
            dynamic: If True, the system prompt will be reevaluated even when `messages_history` is provided,
                see [`SystemPromptPart.dynamic_ref`][pydantic_ai.messages.SystemPromptPart.dynamic_ref]

        Example:
        ```python
        from pydantic_ai import Agent, RunContext

        agent = Agent('test', deps_type=str)

        @agent.system_prompt
        def simple_system_prompt() -> str:
            return 'foobar'

        @agent.system_prompt(dynamic=True)
        async def async_system_prompt(ctx: RunContext[str]) -> str:
            return f'{ctx.deps} is the best'
        ```
        """
        if func is None:

            def decorator(
                func_: _system_prompt.SystemPromptFunc[AgentDepsT],
            ) -> _system_prompt.SystemPromptFunc[AgentDepsT]:
                runner = _system_prompt.SystemPromptRunner[AgentDepsT](func_, dynamic=dynamic)
                self._system_prompt_functions.append(runner)
                if dynamic:
                    self._system_prompt_dynamic_functions[func_.__qualname__] = runner
                return func_

            return decorator
        else:
            assert not dynamic, "dynamic can't be True in this case"
            self._system_prompt_functions.append(_system_prompt.SystemPromptRunner[AgentDepsT](func, dynamic=dynamic))
            return func

    @overload
    def result_validator(
        self, func: Callable[[RunContext[AgentDepsT], ResultDataT], ResultDataT], /
    ) -> Callable[[RunContext[AgentDepsT], ResultDataT], ResultDataT]: ...

    @overload
    def result_validator(
        self, func: Callable[[RunContext[AgentDepsT], ResultDataT], Awaitable[ResultDataT]], /
    ) -> Callable[[RunContext[AgentDepsT], ResultDataT], Awaitable[ResultDataT]]: ...

    @overload
    def result_validator(
        self, func: Callable[[ResultDataT], ResultDataT], /
    ) -> Callable[[ResultDataT], ResultDataT]: ...

    @overload
    def result_validator(
        self, func: Callable[[ResultDataT], Awaitable[ResultDataT]], /
    ) -> Callable[[ResultDataT], Awaitable[ResultDataT]]: ...

    def result_validator(
        self, func: _result.ResultValidatorFunc[AgentDepsT, ResultDataT], /
    ) -> _result.ResultValidatorFunc[AgentDepsT, ResultDataT]:
        """Decorator to register a result validator function.

        Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.
        Can decorate a sync or async functions.

        Overloads for every possible signature of `result_validator` are included so the decorator doesn't obscure
        the type of the function, see `tests/typed_agent.py` for tests.

        Example:
        ```python
        from pydantic_ai import Agent, ModelRetry, RunContext

        agent = Agent('test', deps_type=str)

        @agent.result_validator
        def result_validator_simple(data: str) -> str:
            if 'wrong' in data:
                raise ModelRetry('wrong response')
            return data

        @agent.result_validator
        async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
            if ctx.deps in data:
                raise ModelRetry('wrong response')
            return data

        result = agent.run_sync('foobar', deps='spam')
        print(result.data)
        #> success (no tool calls)
        ```
        """
        self._result_validators.append(_result.ResultValidator[AgentDepsT, Any](func))
        return func

    @overload
    def tool(self, func: ToolFuncContext[AgentDepsT, ToolParams], /) -> ToolFuncContext[AgentDepsT, ToolParams]: ...

    @overload
    def tool(
        self,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ) -> Callable[[ToolFuncContext[AgentDepsT, ToolParams]], ToolFuncContext[AgentDepsT, ToolParams]]: ...

    def tool(
        self,
        func: ToolFuncContext[AgentDepsT, ToolParams] | None = None,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ) -> Any:
        """Decorator to register a tool function which takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.

        Can decorate a sync or async functions.

        The docstring is inspected to extract both the tool description and description of each parameter,
        [learn more](../tools.md#function-tools-and-schema).

        We can't add overloads for every possible signature of tool, since the return type is a recursive union
        so the signature of functions decorated with `@agent.tool` is obscured.

        Example:
        ```python
        from pydantic_ai import Agent, RunContext

        agent = Agent('test', deps_type=int)

        @agent.tool
        def foobar(ctx: RunContext[int], x: int) -> int:
            return ctx.deps + x

        @agent.tool(retries=2)
        async def spam(ctx: RunContext[str], y: float) -> float:
            return ctx.deps + y

        result = agent.run_sync('foobar', deps=1)
        print(result.data)
        #> {"foobar":1,"spam":1.0}
        ```

        Args:
            func: The tool function to register.
            retries: The number of retries to allow for this tool, defaults to the agent's default retries,
                which defaults to 1.
            prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                tool from a given step. This is useful if you want to customise a tool at call time,
                or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
            docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
                Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
            require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
        """
        if func is None:

            def tool_decorator(
                func_: ToolFuncContext[AgentDepsT, ToolParams],
            ) -> ToolFuncContext[AgentDepsT, ToolParams]:
                # noinspection PyTypeChecker
                self._register_function(func_, True, retries, prepare, docstring_format, require_parameter_descriptions)
                return func_

            return tool_decorator
        else:
            # noinspection PyTypeChecker
            self._register_function(func, True, retries, prepare, docstring_format, require_parameter_descriptions)
            return func

    @overload
    def tool_plain(self, func: ToolFuncPlain[ToolParams], /) -> ToolFuncPlain[ToolParams]: ...

    @overload
    def tool_plain(
        self,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ) -> Callable[[ToolFuncPlain[ToolParams]], ToolFuncPlain[ToolParams]]: ...

    def tool_plain(
        self,
        func: ToolFuncPlain[ToolParams] | None = None,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ) -> Any:
        """Decorator to register a tool function which DOES NOT take `RunContext` as an argument.

        Can decorate a sync or async functions.

        The docstring is inspected to extract both the tool description and description of each parameter,
        [learn more](../tools.md#function-tools-and-schema).

        We can't add overloads for every possible signature of tool, since the return type is a recursive union
        so the signature of functions decorated with `@agent.tool` is obscured.

        Example:
        ```python
        from pydantic_ai import Agent, RunContext

        agent = Agent('test')

        @agent.tool
        def foobar(ctx: RunContext[int]) -> int:
            return 123

        @agent.tool(retries=2)
        async def spam(ctx: RunContext[str]) -> float:
            return 3.14

        result = agent.run_sync('foobar', deps=1)
        print(result.data)
        #> {"foobar":123,"spam":3.14}
        ```

        Args:
            func: The tool function to register.
            retries: The number of retries to allow for this tool, defaults to the agent's default retries,
                which defaults to 1.
            prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                tool from a given step. This is useful if you want to customise a tool at call time,
                or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
            docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
                Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
            require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
        """
        if func is None:

            def tool_decorator(func_: ToolFuncPlain[ToolParams]) -> ToolFuncPlain[ToolParams]:
                # noinspection PyTypeChecker
                self._register_function(
                    func_, False, retries, prepare, docstring_format, require_parameter_descriptions
                )
                return func_

            return tool_decorator
        else:
            self._register_function(func, False, retries, prepare, docstring_format, require_parameter_descriptions)
            return func

    def _register_function(
        self,
        func: ToolFuncEither[AgentDepsT, ToolParams],
        takes_ctx: bool,
        retries: int | None,
        prepare: ToolPrepareFunc[AgentDepsT] | None,
        docstring_format: DocstringFormat,
        require_parameter_descriptions: bool,
    ) -> None:
        """Private utility to register a function as a tool."""
        retries_ = retries if retries is not None else self._default_retries
        tool = Tool[AgentDepsT](
            func,
            takes_ctx=takes_ctx,
            max_retries=retries_,
            prepare=prepare,
            docstring_format=docstring_format,
            require_parameter_descriptions=require_parameter_descriptions,
        )
        self._register_tool(tool)

    def _register_tool(self, tool: Tool[AgentDepsT]) -> None:
        """Private utility to register a tool instance."""
        if tool.max_retries is None:
            # noinspection PyTypeChecker
            tool = dataclasses.replace(tool, max_retries=self._default_retries)

        if tool.name in self._function_tools:
            raise exceptions.UserError(f'Tool name conflicts with existing tool: {tool.name!r}')

        if self._result_schema and tool.name in self._result_schema.tools:
            raise exceptions.UserError(f'Tool name conflicts with result schema name: {tool.name!r}')

        self._function_tools[tool.name] = tool

    def _get_model(self, model: models.Model | models.KnownModelName | None) -> models.Model:
        """Create a model configured for this agent.

        Args:
            model: model to use for this run, required if `model` was not set when creating the agent.

        Returns:
            The model used
        """
        model_: models.Model
        if some_model := self._override_model:
            # we don't want `override()` to cover up errors from the model not being defined, hence this check
            if model is None and self.model is None:
                raise exceptions.UserError(
                    '`model` must be set either when creating the agent or when calling it. '
                    '(Even when `override(model=...)` is customizing the model that will actually be called)'
                )
            model_ = some_model.value
        elif model is not None:
            model_ = models.infer_model(model)
        elif self.model is not None:
            # noinspection PyTypeChecker
            model_ = self.model = models.infer_model(self.model)
        else:
            raise exceptions.UserError('`model` must be set either when creating the agent or when calling it.')

        instrument = self.instrument
        if instrument is None:
            instrument = self._instrument_default

        if instrument and not isinstance(model_, InstrumentedModel):
            if instrument is True:
                instrument = InstrumentationSettings()

            model_ = InstrumentedModel(model_, instrument)

        return model_

    def _get_deps(self: Agent[T, ResultDataT], deps: T) -> T:
        """Get deps for a run.

        If we've overridden deps via `_override_deps`, use that, otherwise use the deps passed to the call.

        We could do runtime type checking of deps against `self._deps_type`, but that's a slippery slope.
        """
        if some_deps := self._override_deps:
            return some_deps.value
        else:
            return deps

    def _infer_name(self, function_frame: FrameType | None) -> None:
        """Infer the agent name from the call frame.

        Usage should be `self._infer_name(inspect.currentframe())`.
        """
        assert self.name is None, 'Name already set'
        if function_frame is not None:  # pragma: no branch
            if parent_frame := function_frame.f_back:  # pragma: no branch
                for name, item in parent_frame.f_locals.items():
                    if item is self:
                        self.name = name
                        return
                if parent_frame.f_locals != parent_frame.f_globals:
                    # if we couldn't find the agent in locals and globals are a different dict, try globals
                    for name, item in parent_frame.f_globals.items():
                        if item is self:
                            self.name = name
                            return

    @property
    @deprecated(
        'The `last_run_messages` attribute has been removed, use `capture_run_messages` instead.', category=None
    )
    def last_run_messages(self) -> list[_messages.ModelMessage]:
        raise AttributeError('The `last_run_messages` attribute has been removed, use `capture_run_messages` instead.')

    def _build_graph(
        self, result_type: type[RunResultDataT] | None
    ) -> Graph[_agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any], FinalResult[Any]]:
        return _agent_graph.build_agent_graph(self.name, self._deps_type, result_type or self.result_type)

    def _prepare_result_schema(
        self, result_type: type[RunResultDataT] | None
    ) -> _result.ResultSchema[RunResultDataT] | None:
        if result_type is not None:
            if self._result_validators:
                raise exceptions.UserError('Cannot set a custom run `result_type` when the agent has result validators')
            return _result.ResultSchema[result_type].build(
                result_type, self._result_tool_name, self._result_tool_description
            )
        else:
            return self._result_schema  # pyright: ignore[reportReturnType]

    @staticmethod
    def is_model_request_node(
        node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
    ) -> TypeGuard[_agent_graph.ModelRequestNode[T, S]]:
        """Check if the node is a `ModelRequestNode`, narrowing the type if it is.

        This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
        """
        return isinstance(node, _agent_graph.ModelRequestNode)

    @staticmethod
    def is_call_tools_node(
        node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
    ) -> TypeGuard[_agent_graph.CallToolsNode[T, S]]:
        """Check if the node is a `CallToolsNode`, narrowing the type if it is.

        This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
        """
        return isinstance(node, _agent_graph.CallToolsNode)

    @staticmethod
    def is_user_prompt_node(
        node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
    ) -> TypeGuard[_agent_graph.UserPromptNode[T, S]]:
        """Check if the node is a `UserPromptNode`, narrowing the type if it is.

        This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
        """
        return isinstance(node, _agent_graph.UserPromptNode)

    @staticmethod
    def is_end_node(
        node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
    ) -> TypeGuard[End[result.FinalResult[S]]]:
        """Check if the node is a `End`, narrowing the type if it is.

        This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
        """
        return isinstance(node, End)
```

#### model

instance-attribute

```
instance-attribute
```

```
model: Model | KnownModelName | None
```

```
model: Model | KnownModelName | None
```

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

The default model configured for this agent.

#### __init__

```
__init__(
    model: Model | KnownModelName | None = None,
    *,
    result_type: type[ResultDataT] = str,
    system_prompt: str | Sequence[str] = (),
    deps_type: type[AgentDepsT] = NoneType,
    name: str | None = None,
    model_settings: ModelSettings | None = None,
    retries: int = 1,
    result_tool_name: str = "final_result",
    result_tool_description: str | None = None,
    result_retries: int | None = None,
    tools: Sequence[
        Tool[AgentDepsT] | ToolFuncEither[AgentDepsT, ...]
    ] = (),
    defer_model_check: bool = False,
    end_strategy: EndStrategy = "early",
    instrument: InstrumentationSettings | bool | None = None
)
```

```
__init__(
    model: Model | KnownModelName | None = None,
    *,
    result_type: type[ResultDataT] = str,
    system_prompt: str | Sequence[str] = (),
    deps_type: type[AgentDepsT] = NoneType,
    name: str | None = None,
    model_settings: ModelSettings | None = None,
    retries: int = 1,
    result_tool_name: str = "final_result",
    result_tool_description: str | None = None,
    result_retries: int | None = None,
    tools: Sequence[
        Tool[AgentDepsT] | ToolFuncEither[AgentDepsT, ...]
    ] = (),
    defer_model_check: bool = False,
    end_strategy: EndStrategy = "early",
    instrument: InstrumentationSettings | bool | None = None
)
```

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[type](https://docs.python.org/3/library/functions.html#type)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[type](https://docs.python.org/3/library/functions.html#type)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[int](https://docs.python.org/3/library/functions.html#int)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[int](https://docs.python.org/3/library/functions.html#int)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[Tool](https://ai.pydantic.dev/tools/#pydantic_ai.tools.Tool)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ToolFuncEither](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncEither)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[bool](https://docs.python.org/3/library/functions.html#bool)

[EndStrategy](https://ai.pydantic.dev#pydantic_ai.agent.EndStrategy)

[InstrumentationSettings](https://ai.pydantic.dev#pydantic_ai.agent.InstrumentationSettings)

[bool](https://docs.python.org/3/library/functions.html#bool)

Create an agent.

Parameters:

```
model
```

```
Model | KnownModelName | None
```

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

The default model to use for this agent, if not provide,
you must provide the model when calling it.

```
None
```

```
result_type
```

```
type[ResultDataT]
```

[type](https://docs.python.org/3/library/functions.html#type)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

The type of the result data, used to validate the result data, defaults to str.

```
str
```

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
system_prompt
```

```
str | Sequence[str]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Static system prompts to use for this agent, you can also register system
prompts via a function with system_prompt.

```
system_prompt
```

```
()
```

```
deps_type
```

```
type[AgentDepsT]
```

[type](https://docs.python.org/3/library/functions.html#type)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

The type used for dependency injection, this parameter exists solely to allow you to fully
parameterize the agent, and therefore get the best out of static type checking.
If you're not using deps, but want type checking to pass, you can set deps=None to satisfy Pyright
or add a type hint : Agent[None, <return type>].

```
deps=None
```

```
: Agent[None, <return type>]
```

```
NoneType
```

```
name
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The name of the agent, used for logging. If None, we try to infer the agent name from the call frame
when the agent is first run.

```
None
```

```
None
```

```
model_settings
```

```
ModelSettings | None
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Optional model request settings to use for this agent's runs, by default.

```
None
```

```
retries
```

```
int
```

[int](https://docs.python.org/3/library/functions.html#int)

The default number of retries to allow before raising an error.

```
1
```

```
result_tool_name
```

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The name of the tool to use for the final result.

```
'final_result'
```

```
result_tool_description
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The description of the final result tool.

```
None
```

```
result_retries
```

```
int | None
```

[int](https://docs.python.org/3/library/functions.html#int)

The maximum number of retries to allow for result validation, defaults to retries.

```
retries
```

```
None
```

```
tools
```

```
Sequence[Tool[AgentDepsT] | ToolFuncEither[AgentDepsT, ...]]
```

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[Tool](https://ai.pydantic.dev/tools/#pydantic_ai.tools.Tool)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ToolFuncEither](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncEither)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

Tools to register with the agent, you can also register tools via the decorators
@agent.tool and @agent.tool_plain.

```
@agent.tool
```

```
@agent.tool_plain
```

```
()
```

```
defer_model_check
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

by default, if you provide a named model,
it's evaluated to create a Model instance immediately,
which checks for the necessary environment variables. Set this to false
to defer the evaluation until the first run. Useful if you want to
override the model for testing.

```
Model
```

```
false
```

```
False
```

```
end_strategy
```

```
EndStrategy
```

[EndStrategy](https://ai.pydantic.dev#pydantic_ai.agent.EndStrategy)

Strategy for handling tool calls that are requested alongside a final result.
See EndStrategy for more information.

```
EndStrategy
```

```
'early'
```

```
instrument
```

```
InstrumentationSettings | bool | None
```

[InstrumentationSettings](https://ai.pydantic.dev#pydantic_ai.agent.InstrumentationSettings)

[bool](https://docs.python.org/3/library/functions.html#bool)

Set to True to automatically instrument with OpenTelemetry,
which will use Logfire if it's configured.
Set to an instance of InstrumentationSettings to customize.
If this isn't set, then the last value set by
Agent.instrument_all()
will be used, which defaults to False.

```
InstrumentationSettings
```

```
Agent.instrument_all()
```

```
None
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
```

```
def __init__(
    self,
    model: models.Model | models.KnownModelName | None = None,
    *,
    result_type: type[ResultDataT] = str,
    system_prompt: str | Sequence[str] = (),
    deps_type: type[AgentDepsT] = NoneType,
    name: str | None = None,
    model_settings: ModelSettings | None = None,
    retries: int = 1,
    result_tool_name: str = 'final_result',
    result_tool_description: str | None = None,
    result_retries: int | None = None,
    tools: Sequence[Tool[AgentDepsT] | ToolFuncEither[AgentDepsT, ...]] = (),
    defer_model_check: bool = False,
    end_strategy: EndStrategy = 'early',
    instrument: InstrumentationSettings | bool | None = None,
):
    """Create an agent.

    Args:
        model: The default model to use for this agent, if not provide,
            you must provide the model when calling it.
        result_type: The type of the result data, used to validate the result data, defaults to `str`.
        system_prompt: Static system prompts to use for this agent, you can also register system
            prompts via a function with [`system_prompt`][pydantic_ai.Agent.system_prompt].
        deps_type: The type used for dependency injection, this parameter exists solely to allow you to fully
            parameterize the agent, and therefore get the best out of static type checking.
            If you're not using deps, but want type checking to pass, you can set `deps=None` to satisfy Pyright
            or add a type hint `: Agent[None, <return type>]`.
        name: The name of the agent, used for logging. If `None`, we try to infer the agent name from the call frame
            when the agent is first run.
        model_settings: Optional model request settings to use for this agent's runs, by default.
        retries: The default number of retries to allow before raising an error.
        result_tool_name: The name of the tool to use for the final result.
        result_tool_description: The description of the final result tool.
        result_retries: The maximum number of retries to allow for result validation, defaults to `retries`.
        tools: Tools to register with the agent, you can also register tools via the decorators
            [`@agent.tool`][pydantic_ai.Agent.tool] and [`@agent.tool_plain`][pydantic_ai.Agent.tool_plain].
        defer_model_check: by default, if you provide a [named][pydantic_ai.models.KnownModelName] model,
            it's evaluated to create a [`Model`][pydantic_ai.models.Model] instance immediately,
            which checks for the necessary environment variables. Set this to `false`
            to defer the evaluation until the first run. Useful if you want to
            [override the model][pydantic_ai.Agent.override] for testing.
        end_strategy: Strategy for handling tool calls that are requested alongside a final result.
            See [`EndStrategy`][pydantic_ai.agent.EndStrategy] for more information.
        instrument: Set to True to automatically instrument with OpenTelemetry,
            which will use Logfire if it's configured.
            Set to an instance of [`InstrumentationSettings`][pydantic_ai.agent.InstrumentationSettings] to customize.
            If this isn't set, then the last value set by
            [`Agent.instrument_all()`][pydantic_ai.Agent.instrument_all]
            will be used, which defaults to False.
    """
    if model is None or defer_model_check:
        self.model = model
    else:
        self.model = models.infer_model(model)

    self.end_strategy = end_strategy
    self.name = name
    self.model_settings = model_settings
    self.result_type = result_type
    self.instrument = instrument

    self._deps_type = deps_type

    self._result_tool_name = result_tool_name
    self._result_tool_description = result_tool_description
    self._result_schema: _result.ResultSchema[ResultDataT] | None = _result.ResultSchema[result_type].build(
        result_type, result_tool_name, result_tool_description
    )
    self._result_validators: list[_result.ResultValidator[AgentDepsT, ResultDataT]] = []

    self._system_prompts = (system_prompt,) if isinstance(system_prompt, str) else tuple(system_prompt)
    self._system_prompt_functions: list[_system_prompt.SystemPromptRunner[AgentDepsT]] = []
    self._system_prompt_dynamic_functions: dict[str, _system_prompt.SystemPromptRunner[AgentDepsT]] = {}

    self._function_tools: dict[str, Tool[AgentDepsT]] = {}

    self._default_retries = retries
    self._max_result_retries = result_retries if result_retries is not None else retries
    for tool in tools:
        if isinstance(tool, Tool):
            self._register_tool(tool)
        else:
            self._register_tool(Tool(tool))
```

```
def __init__(
    self,
    model: models.Model | models.KnownModelName | None = None,
    *,
    result_type: type[ResultDataT] = str,
    system_prompt: str | Sequence[str] = (),
    deps_type: type[AgentDepsT] = NoneType,
    name: str | None = None,
    model_settings: ModelSettings | None = None,
    retries: int = 1,
    result_tool_name: str = 'final_result',
    result_tool_description: str | None = None,
    result_retries: int | None = None,
    tools: Sequence[Tool[AgentDepsT] | ToolFuncEither[AgentDepsT, ...]] = (),
    defer_model_check: bool = False,
    end_strategy: EndStrategy = 'early',
    instrument: InstrumentationSettings | bool | None = None,
):
    """Create an agent.

    Args:
        model: The default model to use for this agent, if not provide,
            you must provide the model when calling it.
        result_type: The type of the result data, used to validate the result data, defaults to `str`.
        system_prompt: Static system prompts to use for this agent, you can also register system
            prompts via a function with [`system_prompt`][pydantic_ai.Agent.system_prompt].
        deps_type: The type used for dependency injection, this parameter exists solely to allow you to fully
            parameterize the agent, and therefore get the best out of static type checking.
            If you're not using deps, but want type checking to pass, you can set `deps=None` to satisfy Pyright
            or add a type hint `: Agent[None, <return type>]`.
        name: The name of the agent, used for logging. If `None`, we try to infer the agent name from the call frame
            when the agent is first run.
        model_settings: Optional model request settings to use for this agent's runs, by default.
        retries: The default number of retries to allow before raising an error.
        result_tool_name: The name of the tool to use for the final result.
        result_tool_description: The description of the final result tool.
        result_retries: The maximum number of retries to allow for result validation, defaults to `retries`.
        tools: Tools to register with the agent, you can also register tools via the decorators
            [`@agent.tool`][pydantic_ai.Agent.tool] and [`@agent.tool_plain`][pydantic_ai.Agent.tool_plain].
        defer_model_check: by default, if you provide a [named][pydantic_ai.models.KnownModelName] model,
            it's evaluated to create a [`Model`][pydantic_ai.models.Model] instance immediately,
            which checks for the necessary environment variables. Set this to `false`
            to defer the evaluation until the first run. Useful if you want to
            [override the model][pydantic_ai.Agent.override] for testing.
        end_strategy: Strategy for handling tool calls that are requested alongside a final result.
            See [`EndStrategy`][pydantic_ai.agent.EndStrategy] for more information.
        instrument: Set to True to automatically instrument with OpenTelemetry,
            which will use Logfire if it's configured.
            Set to an instance of [`InstrumentationSettings`][pydantic_ai.agent.InstrumentationSettings] to customize.
            If this isn't set, then the last value set by
            [`Agent.instrument_all()`][pydantic_ai.Agent.instrument_all]
            will be used, which defaults to False.
    """
    if model is None or defer_model_check:
        self.model = model
    else:
        self.model = models.infer_model(model)

    self.end_strategy = end_strategy
    self.name = name
    self.model_settings = model_settings
    self.result_type = result_type
    self.instrument = instrument

    self._deps_type = deps_type

    self._result_tool_name = result_tool_name
    self._result_tool_description = result_tool_description
    self._result_schema: _result.ResultSchema[ResultDataT] | None = _result.ResultSchema[result_type].build(
        result_type, result_tool_name, result_tool_description
    )
    self._result_validators: list[_result.ResultValidator[AgentDepsT, ResultDataT]] = []

    self._system_prompts = (system_prompt,) if isinstance(system_prompt, str) else tuple(system_prompt)
    self._system_prompt_functions: list[_system_prompt.SystemPromptRunner[AgentDepsT]] = []
    self._system_prompt_dynamic_functions: dict[str, _system_prompt.SystemPromptRunner[AgentDepsT]] = {}

    self._function_tools: dict[str, Tool[AgentDepsT]] = {}

    self._default_retries = retries
    self._max_result_retries = result_retries if result_retries is not None else retries
    for tool in tools:
        if isinstance(tool, Tool):
            self._register_tool(tool)
        else:
            self._register_tool(Tool(tool))
```

#### end_strategy

instance-attribute

```
instance-attribute
```

```
end_strategy: EndStrategy = end_strategy
```

```
end_strategy: EndStrategy = end_strategy
```

[EndStrategy](https://ai.pydantic.dev#pydantic_ai.agent.EndStrategy)

Strategy for handling tool calls when a final result is found.

#### name

instance-attribute

```
instance-attribute
```

```
name: str | None = name
```

```
name: str | None = name
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The name of the agent, used for logging.

If None, we try to infer the agent name from the call frame when the agent is first run.

```
None
```

#### model_settings

instance-attribute

```
instance-attribute
```

```
model_settings: ModelSettings | None = model_settings
```

```
model_settings: ModelSettings | None = model_settings
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Optional model request settings to use for this agents's runs, by default.

Note, if model_settings is provided by run, run_sync, or run_stream, those settings will
be merged with this value, with the runtime argument taking priority.

```
model_settings
```

```
run
```

```
run_sync
```

```
run_stream
```

#### result_type

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
result_type: type[ResultDataT] = result_type
```

```
result_type: type[ResultDataT] = result_type
```

[type](https://docs.python.org/3/library/functions.html#type)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

The type of the result data, used to validate the result data, defaults to str.

```
str
```

#### instrument

instance-attribute

```
instance-attribute
```

```
instrument: InstrumentationSettings | bool | None = (
    instrument
)
```

```
instrument: InstrumentationSettings | bool | None = (
    instrument
)
```

[InstrumentationSettings](https://ai.pydantic.dev#pydantic_ai.agent.InstrumentationSettings)

[bool](https://docs.python.org/3/library/functions.html#bool)

Options to automatically instrument with OpenTelemetry.

#### instrument_all

staticmethod

```
staticmethod
```

```
instrument_all(
    instrument: InstrumentationSettings | bool = True,
) -> None
```

```
instrument_all(
    instrument: InstrumentationSettings | bool = True,
) -> None
```

[InstrumentationSettings](https://ai.pydantic.dev#pydantic_ai.agent.InstrumentationSettings)

[bool](https://docs.python.org/3/library/functions.html#bool)

Set the instrumentation options for all agents where instrument is not set.

```
instrument
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
224
225
226
227
```

```
@staticmethod
def instrument_all(instrument: InstrumentationSettings | bool = True) -> None:
    """Set the instrumentation options for all agents where `instrument` is not set."""
    Agent._instrument_default = instrument
```

```
@staticmethod
def instrument_all(instrument: InstrumentationSettings | bool = True) -> None:
    """Set the instrumentation options for all agents where `instrument` is not set."""
    Agent._instrument_default = instrument
```

#### run

async

```
async
```

```
run(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[ResultDataT]
```

```
run(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[ResultDataT]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AgentRunResult](https://ai.pydantic.dev#pydantic_ai.agent.AgentRunResult)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

```
run(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT],
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[RunResultDataT]
```

```
run(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT],
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[RunResultDataT]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AgentRunResult](https://ai.pydantic.dev#pydantic_ai.agent.AgentRunResult)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

```
run(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[Any]
```

```
run(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[Any]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AgentRunResult](https://ai.pydantic.dev#pydantic_ai.agent.AgentRunResult)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

Run the agent with a user prompt in async mode.

This method builds an internal agent graph (using system prompts, tools and result schemas) and then
runs the graph to completion. The result of the run is returned.

Example:
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    agent_run = await agent.run('What is the capital of France?')
    print(agent_run.data)
    #> Paris

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    agent_run = await agent.run('What is the capital of France?')
    print(agent_run.data)
    #> Paris
```

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    agent_run = await agent.run('What is the capital of France?')
    print(agent_run.data)
    #> Paris
```

Parameters:

```
user_prompt
```

```
str | Sequence[UserContent]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

User input to start/continue the conversation.

```
result_type
```

```
type[RunResultDataT] | None
```

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

Custom result type to use for this run, result_type may only be used if the agent has no
result validators since result validators would expect an argument that matches the agent's result type.

```
result_type
```

```
None
```

```
message_history
```

```
list[ModelMessage] | None
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

History of the conversation so far.

```
None
```

```
model
```

```
Model | KnownModelName | None
```

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

Optional model to use for this run, required if model was not set when creating the agent.

```
model
```

```
None
```

```
deps
```

```
AgentDepsT
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

Optional dependencies to use for this run.

```
None
```

```
model_settings
```

```
ModelSettings | None
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Optional settings to use for this model's request.

```
None
```

```
usage_limits
```

```
UsageLimits | None
```

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

Optional limits on model request count or token usage.

```
None
```

```
usage
```

```
Usage | None
```

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

Optional usage to start with, useful for resuming a conversation or agents used in tools.

```
None
```

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to try to infer the agent name from the call frame if it's not set.

```
True
```

Returns:

```
AgentRunResult[Any]
```

[AgentRunResult](https://ai.pydantic.dev#pydantic_ai.agent.AgentRunResult)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

The result of the run.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
```

```
async def run(
    self,
    user_prompt: str | Sequence[_messages.UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[_messages.ModelMessage] | None = None,
    model: models.Model | models.KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: _usage.UsageLimits | None = None,
    usage: _usage.Usage | None = None,
    infer_name: bool = True,
) -> AgentRunResult[Any]:
    """Run the agent with a user prompt in async mode.

    This method builds an internal agent graph (using system prompts, tools and result schemas) and then
    runs the graph to completion. The result of the run is returned.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    async def main():
        agent_run = await agent.run('What is the capital of France?')
        print(agent_run.data)
        #> Paris
    ```

    Args:
        user_prompt: User input to start/continue the conversation.
        result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
            result validators since result validators would expect an argument that matches the agent's result type.
        message_history: History of the conversation so far.
        model: Optional model to use for this run, required if `model` was not set when creating the agent.
        deps: Optional dependencies to use for this run.
        model_settings: Optional settings to use for this model's request.
        usage_limits: Optional limits on model request count or token usage.
        usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
        infer_name: Whether to try to infer the agent name from the call frame if it's not set.

    Returns:
        The result of the run.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    async with self.iter(
        user_prompt=user_prompt,
        result_type=result_type,
        message_history=message_history,
        model=model,
        deps=deps,
        model_settings=model_settings,
        usage_limits=usage_limits,
        usage=usage,
    ) as agent_run:
        async for _ in agent_run:
            pass

    assert (final_result := agent_run.result) is not None, 'The graph run did not finish properly'
    return final_result
```

```
async def run(
    self,
    user_prompt: str | Sequence[_messages.UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[_messages.ModelMessage] | None = None,
    model: models.Model | models.KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: _usage.UsageLimits | None = None,
    usage: _usage.Usage | None = None,
    infer_name: bool = True,
) -> AgentRunResult[Any]:
    """Run the agent with a user prompt in async mode.

    This method builds an internal agent graph (using system prompts, tools and result schemas) and then
    runs the graph to completion. The result of the run is returned.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    async def main():
        agent_run = await agent.run('What is the capital of France?')
        print(agent_run.data)
        #> Paris
    ```

    Args:
        user_prompt: User input to start/continue the conversation.
        result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
            result validators since result validators would expect an argument that matches the agent's result type.
        message_history: History of the conversation so far.
        model: Optional model to use for this run, required if `model` was not set when creating the agent.
        deps: Optional dependencies to use for this run.
        model_settings: Optional settings to use for this model's request.
        usage_limits: Optional limits on model request count or token usage.
        usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
        infer_name: Whether to try to infer the agent name from the call frame if it's not set.

    Returns:
        The result of the run.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    async with self.iter(
        user_prompt=user_prompt,
        result_type=result_type,
        message_history=message_history,
        model=model,
        deps=deps,
        model_settings=model_settings,
        usage_limits=usage_limits,
        usage=usage,
    ) as agent_run:
        async for _ in agent_run:
            pass

    assert (final_result := agent_run.result) is not None, 'The graph run did not finish properly'
    return final_result
```

#### iter

async

```
async
```

```
iter(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AsyncIterator[AgentRun[AgentDepsT, Any]]
```

```
iter(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AsyncIterator[AgentRun[AgentDepsT, Any]]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[AgentRun](https://ai.pydantic.dev#pydantic_ai.agent.AgentRun)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

A contextmanager which can be used to iterate over the agent graph's nodes as they are executed.

This method builds an internal agent graph (using system prompts, tools and result schemas) and then returns an
AgentRun object. The AgentRun can be used to async-iterate over the nodes of the graph as they are
executed. This is the API to use if you want to consume the outputs coming from each LLM model response, or the
stream of events coming from the execution of tools.

```
AgentRun
```

```
AgentRun
```

The AgentRun also provides methods to access the full message history, new messages, and usage statistics,
and the final result of the run once it has completed.

```
AgentRun
```

For more details, see the documentation of AgentRun.

```
AgentRun
```

Example:
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    nodes = []
    async with agent.iter('What is the capital of France?') as agent_run:
        async for node in agent_run:
            nodes.append(node)
    print(nodes)
    '''
    [
        ModelRequestNode(
            request=ModelRequest(
                parts=[
                    UserPromptPart(
                        content='What is the capital of France?',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    )
                ],
                kind='request',
            )
        ),
        CallToolsNode(
            model_response=ModelResponse(
                parts=[TextPart(content='Paris', part_kind='text')],
                model_name='gpt-4o',
                timestamp=datetime.datetime(...),
                kind='response',
            )
        ),
        End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
    ]
    '''
    print(agent_run.result.data)
    #> Paris

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    nodes = []
    async with agent.iter('What is the capital of France?') as agent_run:
        async for node in agent_run:
            nodes.append(node)
    print(nodes)
    '''
    [
        ModelRequestNode(
            request=ModelRequest(
                parts=[
                    UserPromptPart(
                        content='What is the capital of France?',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    )
                ],
                kind='request',
            )
        ),
        CallToolsNode(
            model_response=ModelResponse(
                parts=[TextPart(content='Paris', part_kind='text')],
                model_name='gpt-4o',
                timestamp=datetime.datetime(...),
                kind='response',
            )
        ),
        End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
    ]
    '''
    print(agent_run.result.data)
    #> Paris
```

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    nodes = []
    async with agent.iter('What is the capital of France?') as agent_run:
        async for node in agent_run:
            nodes.append(node)
    print(nodes)
    '''
    [
        ModelRequestNode(
            request=ModelRequest(
                parts=[
                    UserPromptPart(
                        content='What is the capital of France?',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    )
                ],
                kind='request',
            )
        ),
        CallToolsNode(
            model_response=ModelResponse(
                parts=[TextPart(content='Paris', part_kind='text')],
                model_name='gpt-4o',
                timestamp=datetime.datetime(...),
                kind='response',
            )
        ),
        End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
    ]
    '''
    print(agent_run.result.data)
    #> Paris
```

Parameters:

```
user_prompt
```

```
str | Sequence[UserContent]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

User input to start/continue the conversation.

```
result_type
```

```
type[RunResultDataT] | None
```

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

Custom result type to use for this run, result_type may only be used if the agent has no
result validators since result validators would expect an argument that matches the agent's result type.

```
result_type
```

```
None
```

```
message_history
```

```
list[ModelMessage] | None
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

History of the conversation so far.

```
None
```

```
model
```

```
Model | KnownModelName | None
```

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

Optional model to use for this run, required if model was not set when creating the agent.

```
model
```

```
None
```

```
deps
```

```
AgentDepsT
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

Optional dependencies to use for this run.

```
None
```

```
model_settings
```

```
ModelSettings | None
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Optional settings to use for this model's request.

```
None
```

```
usage_limits
```

```
UsageLimits | None
```

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

Optional limits on model request count or token usage.

```
None
```

```
usage
```

```
Usage | None
```

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

Optional usage to start with, useful for resuming a conversation or agents used in tools.

```
None
```

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to try to infer the agent name from the call frame if it's not set.

```
True
```

Returns:

```
AsyncIterator[AgentRun[AgentDepsT, Any]]
```

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[AgentRun](https://ai.pydantic.dev#pydantic_ai.agent.AgentRun)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

The result of the run.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
```

```
@asynccontextmanager
async def iter(
    self,
    user_prompt: str | Sequence[_messages.UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[_messages.ModelMessage] | None = None,
    model: models.Model | models.KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: _usage.UsageLimits | None = None,
    usage: _usage.Usage | None = None,
    infer_name: bool = True,
) -> AsyncIterator[AgentRun[AgentDepsT, Any]]:
    """A contextmanager which can be used to iterate over the agent graph's nodes as they are executed.

    This method builds an internal agent graph (using system prompts, tools and result schemas) and then returns an
    `AgentRun` object. The `AgentRun` can be used to async-iterate over the nodes of the graph as they are
    executed. This is the API to use if you want to consume the outputs coming from each LLM model response, or the
    stream of events coming from the execution of tools.

    The `AgentRun` also provides methods to access the full message history, new messages, and usage statistics,
    and the final result of the run once it has completed.

    For more details, see the documentation of `AgentRun`.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    async def main():
        nodes = []
        async with agent.iter('What is the capital of France?') as agent_run:
            async for node in agent_run:
                nodes.append(node)
        print(nodes)
        '''
        [
            ModelRequestNode(
                request=ModelRequest(
                    parts=[
                        UserPromptPart(
                            content='What is the capital of France?',
                            timestamp=datetime.datetime(...),
                            part_kind='user-prompt',
                        )
                    ],
                    kind='request',
                )
            ),
            CallToolsNode(
                model_response=ModelResponse(
                    parts=[TextPart(content='Paris', part_kind='text')],
                    model_name='gpt-4o',
                    timestamp=datetime.datetime(...),
                    kind='response',
                )
            ),
            End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
        ]
        '''
        print(agent_run.result.data)
        #> Paris
    ```

    Args:
        user_prompt: User input to start/continue the conversation.
        result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
            result validators since result validators would expect an argument that matches the agent's result type.
        message_history: History of the conversation so far.
        model: Optional model to use for this run, required if `model` was not set when creating the agent.
        deps: Optional dependencies to use for this run.
        model_settings: Optional settings to use for this model's request.
        usage_limits: Optional limits on model request count or token usage.
        usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
        infer_name: Whether to try to infer the agent name from the call frame if it's not set.

    Returns:
        The result of the run.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    model_used = self._get_model(model)
    del model

    deps = self._get_deps(deps)
    new_message_index = len(message_history) if message_history else 0
    result_schema: _result.ResultSchema[RunResultDataT] | None = self._prepare_result_schema(result_type)

    # Build the graph
    graph = self._build_graph(result_type)

    # Build the initial state
    state = _agent_graph.GraphAgentState(
        message_history=message_history[:] if message_history else [],
        usage=usage or _usage.Usage(),
        retries=0,
        run_step=0,
    )

    # We consider it a user error if a user tries to restrict the result type while having a result validator that
    # may change the result type from the restricted type to something else. Therefore, we consider the following
    # typecast reasonable, even though it is possible to violate it with otherwise-type-checked code.
    result_validators = cast(list[_result.ResultValidator[AgentDepsT, RunResultDataT]], self._result_validators)

    # TODO: Instead of this, copy the function tools to ensure they don't share current_retry state between agent
    #  runs. Requires some changes to `Tool` to make them copyable though.
    for v in self._function_tools.values():
        v.current_retry = 0

    model_settings = merge_model_settings(self.model_settings, model_settings)
    usage_limits = usage_limits or _usage.UsageLimits()

    if isinstance(model_used, InstrumentedModel):
        tracer = model_used.options.tracer
    else:
        tracer = NoOpTracer()
    agent_name = self.name or 'agent'
    run_span = tracer.start_span(
        'agent run',
        attributes={
            'model_name': model_used.model_name if model_used else 'no-model',
            'agent_name': agent_name,
            'logfire.msg': f'{agent_name} run',
        },
    )

    graph_deps = _agent_graph.GraphAgentDeps[AgentDepsT, RunResultDataT](
        user_deps=deps,
        prompt=user_prompt,
        new_message_index=new_message_index,
        model=model_used,
        model_settings=model_settings,
        usage_limits=usage_limits,
        max_result_retries=self._max_result_retries,
        end_strategy=self.end_strategy,
        result_schema=result_schema,
        result_tools=self._result_schema.tool_defs() if self._result_schema else [],
        result_validators=result_validators,
        function_tools=self._function_tools,
        run_span=run_span,
        tracer=tracer,
    )
    start_node = _agent_graph.UserPromptNode[AgentDepsT](
        user_prompt=user_prompt,
        system_prompts=self._system_prompts,
        system_prompt_functions=self._system_prompt_functions,
        system_prompt_dynamic_functions=self._system_prompt_dynamic_functions,
    )

    async with graph.iter(
        start_node,
        state=state,
        deps=graph_deps,
        infer_name=False,
        span=use_span(run_span, end_on_exit=True),
    ) as graph_run:
        yield AgentRun(graph_run)
```

```
@asynccontextmanager
async def iter(
    self,
    user_prompt: str | Sequence[_messages.UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[_messages.ModelMessage] | None = None,
    model: models.Model | models.KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: _usage.UsageLimits | None = None,
    usage: _usage.Usage | None = None,
    infer_name: bool = True,
) -> AsyncIterator[AgentRun[AgentDepsT, Any]]:
    """A contextmanager which can be used to iterate over the agent graph's nodes as they are executed.

    This method builds an internal agent graph (using system prompts, tools and result schemas) and then returns an
    `AgentRun` object. The `AgentRun` can be used to async-iterate over the nodes of the graph as they are
    executed. This is the API to use if you want to consume the outputs coming from each LLM model response, or the
    stream of events coming from the execution of tools.

    The `AgentRun` also provides methods to access the full message history, new messages, and usage statistics,
    and the final result of the run once it has completed.

    For more details, see the documentation of `AgentRun`.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    async def main():
        nodes = []
        async with agent.iter('What is the capital of France?') as agent_run:
            async for node in agent_run:
                nodes.append(node)
        print(nodes)
        '''
        [
            ModelRequestNode(
                request=ModelRequest(
                    parts=[
                        UserPromptPart(
                            content='What is the capital of France?',
                            timestamp=datetime.datetime(...),
                            part_kind='user-prompt',
                        )
                    ],
                    kind='request',
                )
            ),
            CallToolsNode(
                model_response=ModelResponse(
                    parts=[TextPart(content='Paris', part_kind='text')],
                    model_name='gpt-4o',
                    timestamp=datetime.datetime(...),
                    kind='response',
                )
            ),
            End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
        ]
        '''
        print(agent_run.result.data)
        #> Paris
    ```

    Args:
        user_prompt: User input to start/continue the conversation.
        result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
            result validators since result validators would expect an argument that matches the agent's result type.
        message_history: History of the conversation so far.
        model: Optional model to use for this run, required if `model` was not set when creating the agent.
        deps: Optional dependencies to use for this run.
        model_settings: Optional settings to use for this model's request.
        usage_limits: Optional limits on model request count or token usage.
        usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
        infer_name: Whether to try to infer the agent name from the call frame if it's not set.

    Returns:
        The result of the run.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    model_used = self._get_model(model)
    del model

    deps = self._get_deps(deps)
    new_message_index = len(message_history) if message_history else 0
    result_schema: _result.ResultSchema[RunResultDataT] | None = self._prepare_result_schema(result_type)

    # Build the graph
    graph = self._build_graph(result_type)

    # Build the initial state
    state = _agent_graph.GraphAgentState(
        message_history=message_history[:] if message_history else [],
        usage=usage or _usage.Usage(),
        retries=0,
        run_step=0,
    )

    # We consider it a user error if a user tries to restrict the result type while having a result validator that
    # may change the result type from the restricted type to something else. Therefore, we consider the following
    # typecast reasonable, even though it is possible to violate it with otherwise-type-checked code.
    result_validators = cast(list[_result.ResultValidator[AgentDepsT, RunResultDataT]], self._result_validators)

    # TODO: Instead of this, copy the function tools to ensure they don't share current_retry state between agent
    #  runs. Requires some changes to `Tool` to make them copyable though.
    for v in self._function_tools.values():
        v.current_retry = 0

    model_settings = merge_model_settings(self.model_settings, model_settings)
    usage_limits = usage_limits or _usage.UsageLimits()

    if isinstance(model_used, InstrumentedModel):
        tracer = model_used.options.tracer
    else:
        tracer = NoOpTracer()
    agent_name = self.name or 'agent'
    run_span = tracer.start_span(
        'agent run',
        attributes={
            'model_name': model_used.model_name if model_used else 'no-model',
            'agent_name': agent_name,
            'logfire.msg': f'{agent_name} run',
        },
    )

    graph_deps = _agent_graph.GraphAgentDeps[AgentDepsT, RunResultDataT](
        user_deps=deps,
        prompt=user_prompt,
        new_message_index=new_message_index,
        model=model_used,
        model_settings=model_settings,
        usage_limits=usage_limits,
        max_result_retries=self._max_result_retries,
        end_strategy=self.end_strategy,
        result_schema=result_schema,
        result_tools=self._result_schema.tool_defs() if self._result_schema else [],
        result_validators=result_validators,
        function_tools=self._function_tools,
        run_span=run_span,
        tracer=tracer,
    )
    start_node = _agent_graph.UserPromptNode[AgentDepsT](
        user_prompt=user_prompt,
        system_prompts=self._system_prompts,
        system_prompt_functions=self._system_prompt_functions,
        system_prompt_dynamic_functions=self._system_prompt_dynamic_functions,
    )

    async with graph.iter(
        start_node,
        state=state,
        deps=graph_deps,
        infer_name=False,
        span=use_span(run_span, end_on_exit=True),
    ) as graph_run:
        yield AgentRun(graph_run)
```

#### run_sync

```
run_sync(
    user_prompt: str | Sequence[UserContent],
    *,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[ResultDataT]
```

```
run_sync(
    user_prompt: str | Sequence[UserContent],
    *,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[ResultDataT]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AgentRunResult](https://ai.pydantic.dev#pydantic_ai.agent.AgentRunResult)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

```
run_sync(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[RunResultDataT]
```

```
run_sync(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[RunResultDataT]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AgentRunResult](https://ai.pydantic.dev#pydantic_ai.agent.AgentRunResult)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

```
run_sync(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[Any]
```

```
run_sync(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AgentRunResult[Any]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AgentRunResult](https://ai.pydantic.dev#pydantic_ai.agent.AgentRunResult)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

Synchronously run the agent with a user prompt.

This is a convenience method that wraps self.run with loop.run_until_complete(...).
You therefore can't use this method inside async code or if there's an active event loop.

```
self.run
```

```
loop.run_until_complete(...)
```

Example:
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync('What is the capital of Italy?')
print(result_sync.data)
#> Rome

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync('What is the capital of Italy?')
print(result_sync.data)
#> Rome
```

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync('What is the capital of Italy?')
print(result_sync.data)
#> Rome
```

Parameters:

```
user_prompt
```

```
str | Sequence[UserContent]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

User input to start/continue the conversation.

```
result_type
```

```
type[RunResultDataT] | None
```

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

Custom result type to use for this run, result_type may only be used if the agent has no
result validators since result validators would expect an argument that matches the agent's result type.

```
result_type
```

```
None
```

```
message_history
```

```
list[ModelMessage] | None
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

History of the conversation so far.

```
None
```

```
model
```

```
Model | KnownModelName | None
```

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

Optional model to use for this run, required if model was not set when creating the agent.

```
model
```

```
None
```

```
deps
```

```
AgentDepsT
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

Optional dependencies to use for this run.

```
None
```

```
model_settings
```

```
ModelSettings | None
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Optional settings to use for this model's request.

```
None
```

```
usage_limits
```

```
UsageLimits | None
```

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

Optional limits on model request count or token usage.

```
None
```

```
usage
```

```
Usage | None
```

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

Optional usage to start with, useful for resuming a conversation or agents used in tools.

```
None
```

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to try to infer the agent name from the call frame if it's not set.

```
True
```

Returns:

```
AgentRunResult[Any]
```

[AgentRunResult](https://ai.pydantic.dev#pydantic_ai.agent.AgentRunResult)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

The result of the run.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
```

```
def run_sync(
    self,
    user_prompt: str | Sequence[_messages.UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[_messages.ModelMessage] | None = None,
    model: models.Model | models.KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: _usage.UsageLimits | None = None,
    usage: _usage.Usage | None = None,
    infer_name: bool = True,
) -> AgentRunResult[Any]:
    """Synchronously run the agent with a user prompt.

    This is a convenience method that wraps [`self.run`][pydantic_ai.Agent.run] with `loop.run_until_complete(...)`.
    You therefore can't use this method inside async code or if there's an active event loop.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    result_sync = agent.run_sync('What is the capital of Italy?')
    print(result_sync.data)
    #> Rome
    ```

    Args:
        user_prompt: User input to start/continue the conversation.
        result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
            result validators since result validators would expect an argument that matches the agent's result type.
        message_history: History of the conversation so far.
        model: Optional model to use for this run, required if `model` was not set when creating the agent.
        deps: Optional dependencies to use for this run.
        model_settings: Optional settings to use for this model's request.
        usage_limits: Optional limits on model request count or token usage.
        usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
        infer_name: Whether to try to infer the agent name from the call frame if it's not set.

    Returns:
        The result of the run.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    return get_event_loop().run_until_complete(
        self.run(
            user_prompt,
            result_type=result_type,
            message_history=message_history,
            model=model,
            deps=deps,
            model_settings=model_settings,
            usage_limits=usage_limits,
            usage=usage,
            infer_name=False,
        )
    )
```

```
def run_sync(
    self,
    user_prompt: str | Sequence[_messages.UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[_messages.ModelMessage] | None = None,
    model: models.Model | models.KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: _usage.UsageLimits | None = None,
    usage: _usage.Usage | None = None,
    infer_name: bool = True,
) -> AgentRunResult[Any]:
    """Synchronously run the agent with a user prompt.

    This is a convenience method that wraps [`self.run`][pydantic_ai.Agent.run] with `loop.run_until_complete(...)`.
    You therefore can't use this method inside async code or if there's an active event loop.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    result_sync = agent.run_sync('What is the capital of Italy?')
    print(result_sync.data)
    #> Rome
    ```

    Args:
        user_prompt: User input to start/continue the conversation.
        result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
            result validators since result validators would expect an argument that matches the agent's result type.
        message_history: History of the conversation so far.
        model: Optional model to use for this run, required if `model` was not set when creating the agent.
        deps: Optional dependencies to use for this run.
        model_settings: Optional settings to use for this model's request.
        usage_limits: Optional limits on model request count or token usage.
        usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
        infer_name: Whether to try to infer the agent name from the call frame if it's not set.

    Returns:
        The result of the run.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    return get_event_loop().run_until_complete(
        self.run(
            user_prompt,
            result_type=result_type,
            message_history=message_history,
            model=model,
            deps=deps,
            model_settings=model_settings,
            usage_limits=usage_limits,
            usage=usage,
            infer_name=False,
        )
    )
```

#### run_stream

async

```
async
```

```
run_stream(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AbstractAsyncContextManager[
    StreamedRunResult[AgentDepsT, ResultDataT]
]
```

```
run_stream(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AbstractAsyncContextManager[
    StreamedRunResult[AgentDepsT, ResultDataT]
]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AbstractAsyncContextManager](https://docs.python.org/3/library/contextlib.html#contextlib.AbstractAsyncContextManager)

[StreamedRunResult](https://ai.pydantic.dev/result/#pydantic_ai.result.StreamedRunResult)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

```
run_stream(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT],
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AbstractAsyncContextManager[
    StreamedRunResult[AgentDepsT, RunResultDataT]
]
```

```
run_stream(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT],
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AbstractAsyncContextManager[
    StreamedRunResult[AgentDepsT, RunResultDataT]
]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AbstractAsyncContextManager](https://docs.python.org/3/library/contextlib.html#contextlib.AbstractAsyncContextManager)

[StreamedRunResult](https://ai.pydantic.dev/result/#pydantic_ai.result.StreamedRunResult)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

```
run_stream(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AsyncIterator[StreamedRunResult[AgentDepsT, Any]]
```

```
run_stream(
    user_prompt: str | Sequence[UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[ModelMessage] | None = None,
    model: Model | KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: UsageLimits | None = None,
    usage: Usage | None = None,
    infer_name: bool = True
) -> AsyncIterator[StreamedRunResult[AgentDepsT, Any]]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[StreamedRunResult](https://ai.pydantic.dev/result/#pydantic_ai.result.StreamedRunResult)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

Run the agent with a user prompt in async mode, returning a streamed response.

Example:
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    async with agent.run_stream('What is the capital of the UK?') as response:
        print(await response.get_data())
        #> London

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    async with agent.run_stream('What is the capital of the UK?') as response:
        print(await response.get_data())
        #> London
```

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    async with agent.run_stream('What is the capital of the UK?') as response:
        print(await response.get_data())
        #> London
```

Parameters:

```
user_prompt
```

```
str | Sequence[UserContent]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

User input to start/continue the conversation.

```
result_type
```

```
type[RunResultDataT] | None
```

[type](https://docs.python.org/3/library/functions.html#type)

[RunResultDataT](https://ai.pydantic.dev#pydantic_ai.agent.RunResultDataT)

Custom result type to use for this run, result_type may only be used if the agent has no
result validators since result validators would expect an argument that matches the agent's result type.

```
result_type
```

```
None
```

```
message_history
```

```
list[ModelMessage] | None
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

History of the conversation so far.

```
None
```

```
model
```

```
Model | KnownModelName | None
```

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

Optional model to use for this run, required if model was not set when creating the agent.

```
model
```

```
None
```

```
deps
```

```
AgentDepsT
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

Optional dependencies to use for this run.

```
None
```

```
model_settings
```

```
ModelSettings | None
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Optional settings to use for this model's request.

```
None
```

```
usage_limits
```

```
UsageLimits | None
```

[UsageLimits](https://ai.pydantic.dev/usage/#pydantic_ai.usage.UsageLimits)

Optional limits on model request count or token usage.

```
None
```

```
usage
```

```
Usage | None
```

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

Optional usage to start with, useful for resuming a conversation or agents used in tools.

```
None
```

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to try to infer the agent name from the call frame if it's not set.

```
True
```

Returns:

```
AsyncIterator[StreamedRunResult[AgentDepsT, Any]]
```

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[StreamedRunResult](https://ai.pydantic.dev/result/#pydantic_ai.result.StreamedRunResult)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

The result of the run.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
```

```
@asynccontextmanager
async def run_stream(  # noqa C901
    self,
    user_prompt: str | Sequence[_messages.UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[_messages.ModelMessage] | None = None,
    model: models.Model | models.KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: _usage.UsageLimits | None = None,
    usage: _usage.Usage | None = None,
    infer_name: bool = True,
) -> AsyncIterator[result.StreamedRunResult[AgentDepsT, Any]]:
    """Run the agent with a user prompt in async mode, returning a streamed response.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    async def main():
        async with agent.run_stream('What is the capital of the UK?') as response:
            print(await response.get_data())
            #> London
    ```

    Args:
        user_prompt: User input to start/continue the conversation.
        result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
            result validators since result validators would expect an argument that matches the agent's result type.
        message_history: History of the conversation so far.
        model: Optional model to use for this run, required if `model` was not set when creating the agent.
        deps: Optional dependencies to use for this run.
        model_settings: Optional settings to use for this model's request.
        usage_limits: Optional limits on model request count or token usage.
        usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
        infer_name: Whether to try to infer the agent name from the call frame if it's not set.

    Returns:
        The result of the run.
    """
    # TODO: We need to deprecate this now that we have the `iter` method.
    #   Before that, though, we should add an event for when we reach the final result of the stream.
    if infer_name and self.name is None:
        # f_back because `asynccontextmanager` adds one frame
        if frame := inspect.currentframe():  # pragma: no branch
            self._infer_name(frame.f_back)

    yielded = False
    async with self.iter(
        user_prompt,
        result_type=result_type,
        message_history=message_history,
        model=model,
        deps=deps,
        model_settings=model_settings,
        usage_limits=usage_limits,
        usage=usage,
        infer_name=False,
    ) as agent_run:
        first_node = agent_run.next_node  # start with the first node
        assert isinstance(first_node, _agent_graph.UserPromptNode)  # the first node should be a user prompt node
        node = first_node
        while True:
            if self.is_model_request_node(node):
                graph_ctx = agent_run.ctx
                async with node._stream(graph_ctx) as streamed_response:  # pyright: ignore[reportPrivateUsage]

                    async def stream_to_final(
                        s: models.StreamedResponse,
                    ) -> FinalResult[models.StreamedResponse] | None:
                        result_schema = graph_ctx.deps.result_schema
                        async for maybe_part_event in streamed_response:
                            if isinstance(maybe_part_event, _messages.PartStartEvent):
                                new_part = maybe_part_event.part
                                if isinstance(new_part, _messages.TextPart):
                                    if _agent_graph.allow_text_result(result_schema):
                                        return FinalResult(s, None, None)
                                elif isinstance(new_part, _messages.ToolCallPart) and result_schema:
                                    for call, _ in result_schema.find_tool([new_part]):
                                        return FinalResult(s, call.tool_name, call.tool_call_id)
                        return None

                    final_result_details = await stream_to_final(streamed_response)
                    if final_result_details is not None:
                        if yielded:
                            raise exceptions.AgentRunError('Agent run produced final results')
                        yielded = True

                        messages = graph_ctx.state.message_history.copy()

                        async def on_complete() -> None:
                            """Called when the stream has completed.

                            The model response will have been added to messages by now
                            by `StreamedRunResult._marked_completed`.
                            """
                            last_message = messages[-1]
                            assert isinstance(last_message, _messages.ModelResponse)
                            tool_calls = [
                                part for part in last_message.parts if isinstance(part, _messages.ToolCallPart)
                            ]

                            parts: list[_messages.ModelRequestPart] = []
                            async for _event in _agent_graph.process_function_tools(
                                tool_calls,
                                final_result_details.tool_name,
                                final_result_details.tool_call_id,
                                graph_ctx,
                                parts,
                            ):
                                pass
                            # TODO: Should we do something here related to the retry count?
                            #   Maybe we should move the incrementing of the retry count to where we actually make a request?
                            # if any(isinstance(part, _messages.RetryPromptPart) for part in parts):
                            #     ctx.state.increment_retries(ctx.deps.max_result_retries)
                            if parts:
                                messages.append(_messages.ModelRequest(parts))

                        yield StreamedRunResult(
                            messages,
                            graph_ctx.deps.new_message_index,
                            graph_ctx.deps.usage_limits,
                            streamed_response,
                            graph_ctx.deps.result_schema,
                            _agent_graph.build_run_context(graph_ctx),
                            graph_ctx.deps.result_validators,
                            final_result_details.tool_name,
                            on_complete,
                        )
                        break
            next_node = await agent_run.next(node)
            if not isinstance(next_node, _agent_graph.AgentNode):
                raise exceptions.AgentRunError('Should have produced a StreamedRunResult before getting here')
            node = cast(_agent_graph.AgentNode[Any, Any], next_node)

    if not yielded:
        raise exceptions.AgentRunError('Agent run finished without producing a final result')
```

```
@asynccontextmanager
async def run_stream(  # noqa C901
    self,
    user_prompt: str | Sequence[_messages.UserContent],
    *,
    result_type: type[RunResultDataT] | None = None,
    message_history: list[_messages.ModelMessage] | None = None,
    model: models.Model | models.KnownModelName | None = None,
    deps: AgentDepsT = None,
    model_settings: ModelSettings | None = None,
    usage_limits: _usage.UsageLimits | None = None,
    usage: _usage.Usage | None = None,
    infer_name: bool = True,
) -> AsyncIterator[result.StreamedRunResult[AgentDepsT, Any]]:
    """Run the agent with a user prompt in async mode, returning a streamed response.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    async def main():
        async with agent.run_stream('What is the capital of the UK?') as response:
            print(await response.get_data())
            #> London
    ```

    Args:
        user_prompt: User input to start/continue the conversation.
        result_type: Custom result type to use for this run, `result_type` may only be used if the agent has no
            result validators since result validators would expect an argument that matches the agent's result type.
        message_history: History of the conversation so far.
        model: Optional model to use for this run, required if `model` was not set when creating the agent.
        deps: Optional dependencies to use for this run.
        model_settings: Optional settings to use for this model's request.
        usage_limits: Optional limits on model request count or token usage.
        usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
        infer_name: Whether to try to infer the agent name from the call frame if it's not set.

    Returns:
        The result of the run.
    """
    # TODO: We need to deprecate this now that we have the `iter` method.
    #   Before that, though, we should add an event for when we reach the final result of the stream.
    if infer_name and self.name is None:
        # f_back because `asynccontextmanager` adds one frame
        if frame := inspect.currentframe():  # pragma: no branch
            self._infer_name(frame.f_back)

    yielded = False
    async with self.iter(
        user_prompt,
        result_type=result_type,
        message_history=message_history,
        model=model,
        deps=deps,
        model_settings=model_settings,
        usage_limits=usage_limits,
        usage=usage,
        infer_name=False,
    ) as agent_run:
        first_node = agent_run.next_node  # start with the first node
        assert isinstance(first_node, _agent_graph.UserPromptNode)  # the first node should be a user prompt node
        node = first_node
        while True:
            if self.is_model_request_node(node):
                graph_ctx = agent_run.ctx
                async with node._stream(graph_ctx) as streamed_response:  # pyright: ignore[reportPrivateUsage]

                    async def stream_to_final(
                        s: models.StreamedResponse,
                    ) -> FinalResult[models.StreamedResponse] | None:
                        result_schema = graph_ctx.deps.result_schema
                        async for maybe_part_event in streamed_response:
                            if isinstance(maybe_part_event, _messages.PartStartEvent):
                                new_part = maybe_part_event.part
                                if isinstance(new_part, _messages.TextPart):
                                    if _agent_graph.allow_text_result(result_schema):
                                        return FinalResult(s, None, None)
                                elif isinstance(new_part, _messages.ToolCallPart) and result_schema:
                                    for call, _ in result_schema.find_tool([new_part]):
                                        return FinalResult(s, call.tool_name, call.tool_call_id)
                        return None

                    final_result_details = await stream_to_final(streamed_response)
                    if final_result_details is not None:
                        if yielded:
                            raise exceptions.AgentRunError('Agent run produced final results')
                        yielded = True

                        messages = graph_ctx.state.message_history.copy()

                        async def on_complete() -> None:
                            """Called when the stream has completed.

                            The model response will have been added to messages by now
                            by `StreamedRunResult._marked_completed`.
                            """
                            last_message = messages[-1]
                            assert isinstance(last_message, _messages.ModelResponse)
                            tool_calls = [
                                part for part in last_message.parts if isinstance(part, _messages.ToolCallPart)
                            ]

                            parts: list[_messages.ModelRequestPart] = []
                            async for _event in _agent_graph.process_function_tools(
                                tool_calls,
                                final_result_details.tool_name,
                                final_result_details.tool_call_id,
                                graph_ctx,
                                parts,
                            ):
                                pass
                            # TODO: Should we do something here related to the retry count?
                            #   Maybe we should move the incrementing of the retry count to where we actually make a request?
                            # if any(isinstance(part, _messages.RetryPromptPart) for part in parts):
                            #     ctx.state.increment_retries(ctx.deps.max_result_retries)
                            if parts:
                                messages.append(_messages.ModelRequest(parts))

                        yield StreamedRunResult(
                            messages,
                            graph_ctx.deps.new_message_index,
                            graph_ctx.deps.usage_limits,
                            streamed_response,
                            graph_ctx.deps.result_schema,
                            _agent_graph.build_run_context(graph_ctx),
                            graph_ctx.deps.result_validators,
                            final_result_details.tool_name,
                            on_complete,
                        )
                        break
            next_node = await agent_run.next(node)
            if not isinstance(next_node, _agent_graph.AgentNode):
                raise exceptions.AgentRunError('Should have produced a StreamedRunResult before getting here')
            node = cast(_agent_graph.AgentNode[Any, Any], next_node)

    if not yielded:
        raise exceptions.AgentRunError('Agent run finished without producing a final result')
```

#### override

```
override(
    *,
    deps: AgentDepsT | Unset = UNSET,
    model: Model | KnownModelName | Unset = UNSET
) -> Iterator[None]
```

```
override(
    *,
    deps: AgentDepsT | Unset = UNSET,
    model: Model | KnownModelName | Unset = UNSET
) -> Iterator[None]
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

[Iterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)

Context manager to temporarily override agent dependencies and model.

This is particularly useful when testing.
You can find an example of this here.

Parameters:

```
deps
```

```
AgentDepsT | Unset
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

The dependencies to use instead of the dependencies passed to the agent run.

```
UNSET
```

```
model
```

```
Model | KnownModelName | Unset
```

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/models/base/#pydantic_ai.models.KnownModelName)

The model to use instead of the model passed to the agent run.

```
UNSET
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
```

```
@contextmanager
def override(
    self,
    *,
    deps: AgentDepsT | _utils.Unset = _utils.UNSET,
    model: models.Model | models.KnownModelName | _utils.Unset = _utils.UNSET,
) -> Iterator[None]:
    """Context manager to temporarily override agent dependencies and model.

    This is particularly useful when testing.
    You can find an example of this [here](../testing-evals.md#overriding-model-via-pytest-fixtures).

    Args:
        deps: The dependencies to use instead of the dependencies passed to the agent run.
        model: The model to use instead of the model passed to the agent run.
    """
    if _utils.is_set(deps):
        override_deps_before = self._override_deps
        self._override_deps = _utils.Some(deps)
    else:
        override_deps_before = _utils.UNSET

    # noinspection PyTypeChecker
    if _utils.is_set(model):
        override_model_before = self._override_model
        # noinspection PyTypeChecker
        self._override_model = _utils.Some(models.infer_model(model))  # pyright: ignore[reportArgumentType]
    else:
        override_model_before = _utils.UNSET

    try:
        yield
    finally:
        if _utils.is_set(override_deps_before):
            self._override_deps = override_deps_before
        if _utils.is_set(override_model_before):
            self._override_model = override_model_before
```

```
@contextmanager
def override(
    self,
    *,
    deps: AgentDepsT | _utils.Unset = _utils.UNSET,
    model: models.Model | models.KnownModelName | _utils.Unset = _utils.UNSET,
) -> Iterator[None]:
    """Context manager to temporarily override agent dependencies and model.

    This is particularly useful when testing.
    You can find an example of this [here](../testing-evals.md#overriding-model-via-pytest-fixtures).

    Args:
        deps: The dependencies to use instead of the dependencies passed to the agent run.
        model: The model to use instead of the model passed to the agent run.
    """
    if _utils.is_set(deps):
        override_deps_before = self._override_deps
        self._override_deps = _utils.Some(deps)
    else:
        override_deps_before = _utils.UNSET

    # noinspection PyTypeChecker
    if _utils.is_set(model):
        override_model_before = self._override_model
        # noinspection PyTypeChecker
        self._override_model = _utils.Some(models.infer_model(model))  # pyright: ignore[reportArgumentType]
    else:
        override_model_before = _utils.UNSET

    try:
        yield
    finally:
        if _utils.is_set(override_deps_before):
            self._override_deps = override_deps_before
        if _utils.is_set(override_model_before):
            self._override_model = override_model_before
```

#### system_prompt

```
system_prompt(
    func: Callable[[RunContext[AgentDepsT]], str],
) -> Callable[[RunContext[AgentDepsT]], str]
```

```
system_prompt(
    func: Callable[[RunContext[AgentDepsT]], str],
) -> Callable[[RunContext[AgentDepsT]], str]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
system_prompt(
    func: Callable[
        [RunContext[AgentDepsT]], Awaitable[str]
    ],
) -> Callable[[RunContext[AgentDepsT]], Awaitable[str]]
```

```
system_prompt(
    func: Callable[
        [RunContext[AgentDepsT]], Awaitable[str]
    ],
) -> Callable[[RunContext[AgentDepsT]], Awaitable[str]]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
system_prompt(func: Callable[[], str]) -> Callable[[], str]
```

```
system_prompt(func: Callable[[], str]) -> Callable[[], str]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
system_prompt(
    func: Callable[[], Awaitable[str]],
) -> Callable[[], Awaitable[str]]
```

```
system_prompt(
    func: Callable[[], Awaitable[str]],
) -> Callable[[], Awaitable[str]]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
system_prompt(*, dynamic: bool = False) -> Callable[
    [SystemPromptFunc[AgentDepsT]],
    SystemPromptFunc[AgentDepsT],
]
```

```
system_prompt(*, dynamic: bool = False) -> Callable[
    [SystemPromptFunc[AgentDepsT]],
    SystemPromptFunc[AgentDepsT],
]
```

[bool](https://docs.python.org/3/library/functions.html#bool)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[SystemPromptFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.SystemPromptFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[SystemPromptFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.SystemPromptFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

```
system_prompt(
    func: SystemPromptFunc[AgentDepsT] | None = None,
    /,
    *,
    dynamic: bool = False,
) -> (
    Callable[
        [SystemPromptFunc[AgentDepsT]],
        SystemPromptFunc[AgentDepsT],
    ]
    | SystemPromptFunc[AgentDepsT]
)
```

```
system_prompt(
    func: SystemPromptFunc[AgentDepsT] | None = None,
    /,
    *,
    dynamic: bool = False,
) -> (
    Callable[
        [SystemPromptFunc[AgentDepsT]],
        SystemPromptFunc[AgentDepsT],
    ]
    | SystemPromptFunc[AgentDepsT]
)
```

[SystemPromptFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.SystemPromptFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[bool](https://docs.python.org/3/library/functions.html#bool)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[SystemPromptFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.SystemPromptFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[SystemPromptFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.SystemPromptFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[SystemPromptFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.SystemPromptFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

Decorator to register a system prompt function.

Optionally takes RunContext as its only argument.
Can decorate a sync or async functions.

```
RunContext
```

The decorator can be used either bare (agent.system_prompt) or as a function call
(agent.system_prompt(...)), see the examples below.

```
agent.system_prompt
```

```
agent.system_prompt(...)
```

Overloads for every possible signature of system_prompt are included so the decorator doesn't obscure
the type of the function, see tests/typed_agent.py for tests.

```
system_prompt
```

```
tests/typed_agent.py
```

Parameters:

```
func
```

```
SystemPromptFunc[AgentDepsT] | None
```

[SystemPromptFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.SystemPromptFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

The function to decorate

```
None
```

```
dynamic
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

If True, the system prompt will be reevaluated even when messages_history is provided,
see SystemPromptPart.dynamic_ref

```
messages_history
```

```
SystemPromptPart.dynamic_ref
```

```
False
```

Example:
from pydantic_ai import Agent, RunContext

agent = Agent('test', deps_type=str)

@agent.system_prompt
def simple_system_prompt() -> str:
    return 'foobar'

@agent.system_prompt(dynamic=True)
async def async_system_prompt(ctx: RunContext[str]) -> str:
    return f'{ctx.deps} is the best'

```
from pydantic_ai import Agent, RunContext

agent = Agent('test', deps_type=str)

@agent.system_prompt
def simple_system_prompt() -> str:
    return 'foobar'

@agent.system_prompt(dynamic=True)
async def async_system_prompt(ctx: RunContext[str]) -> str:
    return f'{ctx.deps} is the best'
```

```
from pydantic_ai import Agent, RunContext

agent = Agent('test', deps_type=str)

@agent.system_prompt
def simple_system_prompt() -> str:
    return 'foobar'

@agent.system_prompt(dynamic=True)
async def async_system_prompt(ctx: RunContext[str]) -> str:
    return f'{ctx.deps} is the best'
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
```

```
def system_prompt(
    self,
    func: _system_prompt.SystemPromptFunc[AgentDepsT] | None = None,
    /,
    *,
    dynamic: bool = False,
) -> (
    Callable[[_system_prompt.SystemPromptFunc[AgentDepsT]], _system_prompt.SystemPromptFunc[AgentDepsT]]
    | _system_prompt.SystemPromptFunc[AgentDepsT]
):
    """Decorator to register a system prompt function.

    Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its only argument.
    Can decorate a sync or async functions.

    The decorator can be used either bare (`agent.system_prompt`) or as a function call
    (`agent.system_prompt(...)`), see the examples below.

    Overloads for every possible signature of `system_prompt` are included so the decorator doesn't obscure
    the type of the function, see `tests/typed_agent.py` for tests.

    Args:
        func: The function to decorate
        dynamic: If True, the system prompt will be reevaluated even when `messages_history` is provided,
            see [`SystemPromptPart.dynamic_ref`][pydantic_ai.messages.SystemPromptPart.dynamic_ref]

    Example:
    ```python
    from pydantic_ai import Agent, RunContext

    agent = Agent('test', deps_type=str)

    @agent.system_prompt
    def simple_system_prompt() -> str:
        return 'foobar'

    @agent.system_prompt(dynamic=True)
    async def async_system_prompt(ctx: RunContext[str]) -> str:
        return f'{ctx.deps} is the best'
    ```
    """
    if func is None:

        def decorator(
            func_: _system_prompt.SystemPromptFunc[AgentDepsT],
        ) -> _system_prompt.SystemPromptFunc[AgentDepsT]:
            runner = _system_prompt.SystemPromptRunner[AgentDepsT](func_, dynamic=dynamic)
            self._system_prompt_functions.append(runner)
            if dynamic:
                self._system_prompt_dynamic_functions[func_.__qualname__] = runner
            return func_

        return decorator
    else:
        assert not dynamic, "dynamic can't be True in this case"
        self._system_prompt_functions.append(_system_prompt.SystemPromptRunner[AgentDepsT](func, dynamic=dynamic))
        return func
```

```
def system_prompt(
    self,
    func: _system_prompt.SystemPromptFunc[AgentDepsT] | None = None,
    /,
    *,
    dynamic: bool = False,
) -> (
    Callable[[_system_prompt.SystemPromptFunc[AgentDepsT]], _system_prompt.SystemPromptFunc[AgentDepsT]]
    | _system_prompt.SystemPromptFunc[AgentDepsT]
):
    """Decorator to register a system prompt function.

    Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its only argument.
    Can decorate a sync or async functions.

    The decorator can be used either bare (`agent.system_prompt`) or as a function call
    (`agent.system_prompt(...)`), see the examples below.

    Overloads for every possible signature of `system_prompt` are included so the decorator doesn't obscure
    the type of the function, see `tests/typed_agent.py` for tests.

    Args:
        func: The function to decorate
        dynamic: If True, the system prompt will be reevaluated even when `messages_history` is provided,
            see [`SystemPromptPart.dynamic_ref`][pydantic_ai.messages.SystemPromptPart.dynamic_ref]

    Example:
    ```python
    from pydantic_ai import Agent, RunContext

    agent = Agent('test', deps_type=str)

    @agent.system_prompt
    def simple_system_prompt() -> str:
        return 'foobar'

    @agent.system_prompt(dynamic=True)
    async def async_system_prompt(ctx: RunContext[str]) -> str:
        return f'{ctx.deps} is the best'
    ```
    """
    if func is None:

        def decorator(
            func_: _system_prompt.SystemPromptFunc[AgentDepsT],
        ) -> _system_prompt.SystemPromptFunc[AgentDepsT]:
            runner = _system_prompt.SystemPromptRunner[AgentDepsT](func_, dynamic=dynamic)
            self._system_prompt_functions.append(runner)
            if dynamic:
                self._system_prompt_dynamic_functions[func_.__qualname__] = runner
            return func_

        return decorator
    else:
        assert not dynamic, "dynamic can't be True in this case"
        self._system_prompt_functions.append(_system_prompt.SystemPromptRunner[AgentDepsT](func, dynamic=dynamic))
        return func
```

#### result_validator

```
result_validator(
    func: Callable[
        [RunContext[AgentDepsT], ResultDataT], ResultDataT
    ],
) -> Callable[
    [RunContext[AgentDepsT], ResultDataT], ResultDataT
]
```

```
result_validator(
    func: Callable[
        [RunContext[AgentDepsT], ResultDataT], ResultDataT
    ],
) -> Callable[
    [RunContext[AgentDepsT], ResultDataT], ResultDataT
]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

```
result_validator(
    func: Callable[
        [RunContext[AgentDepsT], ResultDataT],
        Awaitable[ResultDataT],
    ],
) -> Callable[
    [RunContext[AgentDepsT], ResultDataT],
    Awaitable[ResultDataT],
]
```

```
result_validator(
    func: Callable[
        [RunContext[AgentDepsT], ResultDataT],
        Awaitable[ResultDataT],
    ],
) -> Callable[
    [RunContext[AgentDepsT], ResultDataT],
    Awaitable[ResultDataT],
]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

```
result_validator(
    func: Callable[[ResultDataT], ResultDataT],
) -> Callable[[ResultDataT], ResultDataT]
```

```
result_validator(
    func: Callable[[ResultDataT], ResultDataT],
) -> Callable[[ResultDataT], ResultDataT]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

```
result_validator(
    func: Callable[[ResultDataT], Awaitable[ResultDataT]],
) -> Callable[[ResultDataT], Awaitable[ResultDataT]]
```

```
result_validator(
    func: Callable[[ResultDataT], Awaitable[ResultDataT]],
) -> Callable[[ResultDataT], Awaitable[ResultDataT]]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

```
result_validator(
    func: ResultValidatorFunc[AgentDepsT, ResultDataT],
) -> ResultValidatorFunc[AgentDepsT, ResultDataT]
```

```
result_validator(
    func: ResultValidatorFunc[AgentDepsT, ResultDataT],
) -> ResultValidatorFunc[AgentDepsT, ResultDataT]
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

Decorator to register a result validator function.

Optionally takes RunContext as its first argument.
Can decorate a sync or async functions.

```
RunContext
```

Overloads for every possible signature of result_validator are included so the decorator doesn't obscure
the type of the function, see tests/typed_agent.py for tests.

```
result_validator
```

```
tests/typed_agent.py
```

Example:
from pydantic_ai import Agent, ModelRetry, RunContext

agent = Agent('test', deps_type=str)

@agent.result_validator
def result_validator_simple(data: str) -> str:
    if 'wrong' in data:
        raise ModelRetry('wrong response')
    return data

@agent.result_validator
async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
    if ctx.deps in data:
        raise ModelRetry('wrong response')
    return data

result = agent.run_sync('foobar', deps='spam')
print(result.data)
#> success (no tool calls)

```
from pydantic_ai import Agent, ModelRetry, RunContext

agent = Agent('test', deps_type=str)

@agent.result_validator
def result_validator_simple(data: str) -> str:
    if 'wrong' in data:
        raise ModelRetry('wrong response')
    return data

@agent.result_validator
async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
    if ctx.deps in data:
        raise ModelRetry('wrong response')
    return data

result = agent.run_sync('foobar', deps='spam')
print(result.data)
#> success (no tool calls)
```

```
from pydantic_ai import Agent, ModelRetry, RunContext

agent = Agent('test', deps_type=str)

@agent.result_validator
def result_validator_simple(data: str) -> str:
    if 'wrong' in data:
        raise ModelRetry('wrong response')
    return data

@agent.result_validator
async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
    if ctx.deps in data:
        raise ModelRetry('wrong response')
    return data

result = agent.run_sync('foobar', deps='spam')
print(result.data)
#> success (no tool calls)
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
```

```
def result_validator(
    self, func: _result.ResultValidatorFunc[AgentDepsT, ResultDataT], /
) -> _result.ResultValidatorFunc[AgentDepsT, ResultDataT]:
    """Decorator to register a result validator function.

    Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.
    Can decorate a sync or async functions.

    Overloads for every possible signature of `result_validator` are included so the decorator doesn't obscure
    the type of the function, see `tests/typed_agent.py` for tests.

    Example:
    ```python
    from pydantic_ai import Agent, ModelRetry, RunContext

    agent = Agent('test', deps_type=str)

    @agent.result_validator
    def result_validator_simple(data: str) -> str:
        if 'wrong' in data:
            raise ModelRetry('wrong response')
        return data

    @agent.result_validator
    async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
        if ctx.deps in data:
            raise ModelRetry('wrong response')
        return data

    result = agent.run_sync('foobar', deps='spam')
    print(result.data)
    #> success (no tool calls)
    ```
    """
    self._result_validators.append(_result.ResultValidator[AgentDepsT, Any](func))
    return func
```

```
def result_validator(
    self, func: _result.ResultValidatorFunc[AgentDepsT, ResultDataT], /
) -> _result.ResultValidatorFunc[AgentDepsT, ResultDataT]:
    """Decorator to register a result validator function.

    Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.
    Can decorate a sync or async functions.

    Overloads for every possible signature of `result_validator` are included so the decorator doesn't obscure
    the type of the function, see `tests/typed_agent.py` for tests.

    Example:
    ```python
    from pydantic_ai import Agent, ModelRetry, RunContext

    agent = Agent('test', deps_type=str)

    @agent.result_validator
    def result_validator_simple(data: str) -> str:
        if 'wrong' in data:
            raise ModelRetry('wrong response')
        return data

    @agent.result_validator
    async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
        if ctx.deps in data:
            raise ModelRetry('wrong response')
        return data

    result = agent.run_sync('foobar', deps='spam')
    print(result.data)
    #> success (no tool calls)
    ```
    """
    self._result_validators.append(_result.ResultValidator[AgentDepsT, Any](func))
    return func
```

#### tool

```
tool(
    func: ToolFuncContext[AgentDepsT, ToolParams],
) -> ToolFuncContext[AgentDepsT, ToolParams]
```

```
tool(
    func: ToolFuncContext[AgentDepsT, ToolParams],
) -> ToolFuncContext[AgentDepsT, ToolParams]
```

[ToolFuncContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

[ToolFuncContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

```
tool(
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False
) -> Callable[
    [ToolFuncContext[AgentDepsT, ToolParams]],
    ToolFuncContext[AgentDepsT, ToolParams],
]
```

```
tool(
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False
) -> Callable[
    [ToolFuncContext[AgentDepsT, ToolParams]],
    ToolFuncContext[AgentDepsT, ToolParams],
]
```

[int](https://docs.python.org/3/library/functions.html#int)

[ToolPrepareFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolPrepareFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[DocstringFormat](https://ai.pydantic.dev/tools/#pydantic_ai.tools.DocstringFormat)

[bool](https://docs.python.org/3/library/functions.html#bool)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[ToolFuncContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

[ToolFuncContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

```
tool(
    func: (
        ToolFuncContext[AgentDepsT, ToolParams] | None
    ) = None,
    /,
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False,
) -> Any
```

```
tool(
    func: (
        ToolFuncContext[AgentDepsT, ToolParams] | None
    ) = None,
    /,
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False,
) -> Any
```

[ToolFuncContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

[int](https://docs.python.org/3/library/functions.html#int)

[ToolPrepareFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolPrepareFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[DocstringFormat](https://ai.pydantic.dev/tools/#pydantic_ai.tools.DocstringFormat)

[bool](https://docs.python.org/3/library/functions.html#bool)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

Decorator to register a tool function which takes RunContext as its first argument.

```
RunContext
```

Can decorate a sync or async functions.

The docstring is inspected to extract both the tool description and description of each parameter,
learn more.

We can't add overloads for every possible signature of tool, since the return type is a recursive union
so the signature of functions decorated with @agent.tool is obscured.

```
@agent.tool
```

Example:
from pydantic_ai import Agent, RunContext

agent = Agent('test', deps_type=int)

@agent.tool
def foobar(ctx: RunContext[int], x: int) -> int:
    return ctx.deps + x

@agent.tool(retries=2)
async def spam(ctx: RunContext[str], y: float) -> float:
    return ctx.deps + y

result = agent.run_sync('foobar', deps=1)
print(result.data)
#> {"foobar":1,"spam":1.0}

```
from pydantic_ai import Agent, RunContext

agent = Agent('test', deps_type=int)

@agent.tool
def foobar(ctx: RunContext[int], x: int) -> int:
    return ctx.deps + x

@agent.tool(retries=2)
async def spam(ctx: RunContext[str], y: float) -> float:
    return ctx.deps + y

result = agent.run_sync('foobar', deps=1)
print(result.data)
#> {"foobar":1,"spam":1.0}
```

```
from pydantic_ai import Agent, RunContext

agent = Agent('test', deps_type=int)

@agent.tool
def foobar(ctx: RunContext[int], x: int) -> int:
    return ctx.deps + x

@agent.tool(retries=2)
async def spam(ctx: RunContext[str], y: float) -> float:
    return ctx.deps + y

result = agent.run_sync('foobar', deps=1)
print(result.data)
#> {"foobar":1,"spam":1.0}
```

Parameters:

```
func
```

```
ToolFuncContext[AgentDepsT, ToolParams] | None
```

[ToolFuncContext](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

The tool function to register.

```
None
```

```
retries
```

```
int | None
```

[int](https://docs.python.org/3/library/functions.html#int)

The number of retries to allow for this tool, defaults to the agent's default retries,
which defaults to 1.

```
None
```

```
prepare
```

```
ToolPrepareFunc[AgentDepsT] | None
```

[ToolPrepareFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolPrepareFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

custom method to prepare the tool definition for each step, return None to omit this
tool from a given step. This is useful if you want to customise a tool at call time,
or omit it completely from a step. See ToolPrepareFunc.

```
None
```

```
ToolPrepareFunc
```

```
None
```

```
docstring_format
```

```
DocstringFormat
```

[DocstringFormat](https://ai.pydantic.dev/tools/#pydantic_ai.tools.DocstringFormat)

The format of the docstring, see DocstringFormat.
Defaults to 'auto', such that the format is inferred from the structure of the docstring.

```
DocstringFormat
```

```
'auto'
```

```
'auto'
```

```
require_parameter_descriptions
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

If True, raise an error if a parameter description is missing. Defaults to False.

```
False
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
931
932
933
934
935
936
937
938
939
940
941
942
943
944
945
946
947
948
949
950
951
952
953
954
955
956
957
958
959
960
961
962
963
964
965
966
967
968
969
970
971
972
973
974
975
976
977
978
979
980
981
982
983
984
985
986
987
988
989
990
991
992
993
994
```

```
def tool(
    self,
    func: ToolFuncContext[AgentDepsT, ToolParams] | None = None,
    /,
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = 'auto',
    require_parameter_descriptions: bool = False,
) -> Any:
    """Decorator to register a tool function which takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.

    Can decorate a sync or async functions.

    The docstring is inspected to extract both the tool description and description of each parameter,
    [learn more](../tools.md#function-tools-and-schema).

    We can't add overloads for every possible signature of tool, since the return type is a recursive union
    so the signature of functions decorated with `@agent.tool` is obscured.

    Example:
    ```python
    from pydantic_ai import Agent, RunContext

    agent = Agent('test', deps_type=int)

    @agent.tool
    def foobar(ctx: RunContext[int], x: int) -> int:
        return ctx.deps + x

    @agent.tool(retries=2)
    async def spam(ctx: RunContext[str], y: float) -> float:
        return ctx.deps + y

    result = agent.run_sync('foobar', deps=1)
    print(result.data)
    #> {"foobar":1,"spam":1.0}
    ```

    Args:
        func: The tool function to register.
        retries: The number of retries to allow for this tool, defaults to the agent's default retries,
            which defaults to 1.
        prepare: custom method to prepare the tool definition for each step, return `None` to omit this
            tool from a given step. This is useful if you want to customise a tool at call time,
            or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
        docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
            Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
        require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
    """
    if func is None:

        def tool_decorator(
            func_: ToolFuncContext[AgentDepsT, ToolParams],
        ) -> ToolFuncContext[AgentDepsT, ToolParams]:
            # noinspection PyTypeChecker
            self._register_function(func_, True, retries, prepare, docstring_format, require_parameter_descriptions)
            return func_

        return tool_decorator
    else:
        # noinspection PyTypeChecker
        self._register_function(func, True, retries, prepare, docstring_format, require_parameter_descriptions)
        return func
```

```
def tool(
    self,
    func: ToolFuncContext[AgentDepsT, ToolParams] | None = None,
    /,
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = 'auto',
    require_parameter_descriptions: bool = False,
) -> Any:
    """Decorator to register a tool function which takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.

    Can decorate a sync or async functions.

    The docstring is inspected to extract both the tool description and description of each parameter,
    [learn more](../tools.md#function-tools-and-schema).

    We can't add overloads for every possible signature of tool, since the return type is a recursive union
    so the signature of functions decorated with `@agent.tool` is obscured.

    Example:
    ```python
    from pydantic_ai import Agent, RunContext

    agent = Agent('test', deps_type=int)

    @agent.tool
    def foobar(ctx: RunContext[int], x: int) -> int:
        return ctx.deps + x

    @agent.tool(retries=2)
    async def spam(ctx: RunContext[str], y: float) -> float:
        return ctx.deps + y

    result = agent.run_sync('foobar', deps=1)
    print(result.data)
    #> {"foobar":1,"spam":1.0}
    ```

    Args:
        func: The tool function to register.
        retries: The number of retries to allow for this tool, defaults to the agent's default retries,
            which defaults to 1.
        prepare: custom method to prepare the tool definition for each step, return `None` to omit this
            tool from a given step. This is useful if you want to customise a tool at call time,
            or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
        docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
            Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
        require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
    """
    if func is None:

        def tool_decorator(
            func_: ToolFuncContext[AgentDepsT, ToolParams],
        ) -> ToolFuncContext[AgentDepsT, ToolParams]:
            # noinspection PyTypeChecker
            self._register_function(func_, True, retries, prepare, docstring_format, require_parameter_descriptions)
            return func_

        return tool_decorator
    else:
        # noinspection PyTypeChecker
        self._register_function(func, True, retries, prepare, docstring_format, require_parameter_descriptions)
        return func
```

#### tool_plain

```
tool_plain(
    func: ToolFuncPlain[ToolParams],
) -> ToolFuncPlain[ToolParams]
```

```
tool_plain(
    func: ToolFuncPlain[ToolParams],
) -> ToolFuncPlain[ToolParams]
```

[ToolFuncPlain](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncPlain)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

[ToolFuncPlain](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncPlain)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

```
tool_plain(
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False
) -> Callable[
    [ToolFuncPlain[ToolParams]], ToolFuncPlain[ToolParams]
]
```

```
tool_plain(
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False
) -> Callable[
    [ToolFuncPlain[ToolParams]], ToolFuncPlain[ToolParams]
]
```

[int](https://docs.python.org/3/library/functions.html#int)

[ToolPrepareFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolPrepareFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[DocstringFormat](https://ai.pydantic.dev/tools/#pydantic_ai.tools.DocstringFormat)

[bool](https://docs.python.org/3/library/functions.html#bool)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[ToolFuncPlain](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncPlain)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

[ToolFuncPlain](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncPlain)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

```
tool_plain(
    func: ToolFuncPlain[ToolParams] | None = None,
    /,
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False,
) -> Any
```

```
tool_plain(
    func: ToolFuncPlain[ToolParams] | None = None,
    /,
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False,
) -> Any
```

[ToolFuncPlain](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncPlain)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

[int](https://docs.python.org/3/library/functions.html#int)

[ToolPrepareFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolPrepareFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[DocstringFormat](https://ai.pydantic.dev/tools/#pydantic_ai.tools.DocstringFormat)

[bool](https://docs.python.org/3/library/functions.html#bool)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

Decorator to register a tool function which DOES NOT take RunContext as an argument.

```
RunContext
```

Can decorate a sync or async functions.

The docstring is inspected to extract both the tool description and description of each parameter,
learn more.

We can't add overloads for every possible signature of tool, since the return type is a recursive union
so the signature of functions decorated with @agent.tool is obscured.

```
@agent.tool
```

Example:
from pydantic_ai import Agent, RunContext

agent = Agent('test')

@agent.tool
def foobar(ctx: RunContext[int]) -> int:
    return 123

@agent.tool(retries=2)
async def spam(ctx: RunContext[str]) -> float:
    return 3.14

result = agent.run_sync('foobar', deps=1)
print(result.data)
#> {"foobar":123,"spam":3.14}

```
from pydantic_ai import Agent, RunContext

agent = Agent('test')

@agent.tool
def foobar(ctx: RunContext[int]) -> int:
    return 123

@agent.tool(retries=2)
async def spam(ctx: RunContext[str]) -> float:
    return 3.14

result = agent.run_sync('foobar', deps=1)
print(result.data)
#> {"foobar":123,"spam":3.14}
```

```
from pydantic_ai import Agent, RunContext

agent = Agent('test')

@agent.tool
def foobar(ctx: RunContext[int]) -> int:
    return 123

@agent.tool(retries=2)
async def spam(ctx: RunContext[str]) -> float:
    return 3.14

result = agent.run_sync('foobar', deps=1)
print(result.data)
#> {"foobar":123,"spam":3.14}
```

Parameters:

```
func
```

```
ToolFuncPlain[ToolParams] | None
```

[ToolFuncPlain](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolFuncPlain)

[ToolParams](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolParams)

The tool function to register.

```
None
```

```
retries
```

```
int | None
```

[int](https://docs.python.org/3/library/functions.html#int)

The number of retries to allow for this tool, defaults to the agent's default retries,
which defaults to 1.

```
None
```

```
prepare
```

```
ToolPrepareFunc[AgentDepsT] | None
```

[ToolPrepareFunc](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolPrepareFunc)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

custom method to prepare the tool definition for each step, return None to omit this
tool from a given step. This is useful if you want to customise a tool at call time,
or omit it completely from a step. See ToolPrepareFunc.

```
None
```

```
ToolPrepareFunc
```

```
None
```

```
docstring_format
```

```
DocstringFormat
```

[DocstringFormat](https://ai.pydantic.dev/tools/#pydantic_ai.tools.DocstringFormat)

The format of the docstring, see DocstringFormat.
Defaults to 'auto', such that the format is inferred from the structure of the docstring.

```
DocstringFormat
```

```
'auto'
```

```
'auto'
```

```
require_parameter_descriptions
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

If True, raise an error if a parameter description is missing. Defaults to False.

```
False
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
```

```
def tool_plain(
    self,
    func: ToolFuncPlain[ToolParams] | None = None,
    /,
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = 'auto',
    require_parameter_descriptions: bool = False,
) -> Any:
    """Decorator to register a tool function which DOES NOT take `RunContext` as an argument.

    Can decorate a sync or async functions.

    The docstring is inspected to extract both the tool description and description of each parameter,
    [learn more](../tools.md#function-tools-and-schema).

    We can't add overloads for every possible signature of tool, since the return type is a recursive union
    so the signature of functions decorated with `@agent.tool` is obscured.

    Example:
    ```python
    from pydantic_ai import Agent, RunContext

    agent = Agent('test')

    @agent.tool
    def foobar(ctx: RunContext[int]) -> int:
        return 123

    @agent.tool(retries=2)
    async def spam(ctx: RunContext[str]) -> float:
        return 3.14

    result = agent.run_sync('foobar', deps=1)
    print(result.data)
    #> {"foobar":123,"spam":3.14}
    ```

    Args:
        func: The tool function to register.
        retries: The number of retries to allow for this tool, defaults to the agent's default retries,
            which defaults to 1.
        prepare: custom method to prepare the tool definition for each step, return `None` to omit this
            tool from a given step. This is useful if you want to customise a tool at call time,
            or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
        docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
            Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
        require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
    """
    if func is None:

        def tool_decorator(func_: ToolFuncPlain[ToolParams]) -> ToolFuncPlain[ToolParams]:
            # noinspection PyTypeChecker
            self._register_function(
                func_, False, retries, prepare, docstring_format, require_parameter_descriptions
            )
            return func_

        return tool_decorator
    else:
        self._register_function(func, False, retries, prepare, docstring_format, require_parameter_descriptions)
        return func
```

```
def tool_plain(
    self,
    func: ToolFuncPlain[ToolParams] | None = None,
    /,
    *,
    retries: int | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = 'auto',
    require_parameter_descriptions: bool = False,
) -> Any:
    """Decorator to register a tool function which DOES NOT take `RunContext` as an argument.

    Can decorate a sync or async functions.

    The docstring is inspected to extract both the tool description and description of each parameter,
    [learn more](../tools.md#function-tools-and-schema).

    We can't add overloads for every possible signature of tool, since the return type is a recursive union
    so the signature of functions decorated with `@agent.tool` is obscured.

    Example:
    ```python
    from pydantic_ai import Agent, RunContext

    agent = Agent('test')

    @agent.tool
    def foobar(ctx: RunContext[int]) -> int:
        return 123

    @agent.tool(retries=2)
    async def spam(ctx: RunContext[str]) -> float:
        return 3.14

    result = agent.run_sync('foobar', deps=1)
    print(result.data)
    #> {"foobar":123,"spam":3.14}
    ```

    Args:
        func: The tool function to register.
        retries: The number of retries to allow for this tool, defaults to the agent's default retries,
            which defaults to 1.
        prepare: custom method to prepare the tool definition for each step, return `None` to omit this
            tool from a given step. This is useful if you want to customise a tool at call time,
            or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
        docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
            Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
        require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
    """
    if func is None:

        def tool_decorator(func_: ToolFuncPlain[ToolParams]) -> ToolFuncPlain[ToolParams]:
            # noinspection PyTypeChecker
            self._register_function(
                func_, False, retries, prepare, docstring_format, require_parameter_descriptions
            )
            return func_

        return tool_decorator
    else:
        self._register_function(func, False, retries, prepare, docstring_format, require_parameter_descriptions)
        return func
```

#### is_model_request_node

staticmethod

```
staticmethod
```

```
is_model_request_node(
    node: AgentNode[T, S] | End[FinalResult[S]],
) -> TypeGuard[ModelRequestNode[T, S]]
```

```
is_model_request_node(
    node: AgentNode[T, S] | End[FinalResult[S]],
) -> TypeGuard[ModelRequestNode[T, S]]
```

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[TypeGuard](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeGuard)

Check if the node is a ModelRequestNode, narrowing the type if it is.

```
ModelRequestNode
```

This method preserves the generic parameters while narrowing the type, unlike a direct call to isinstance.

```
isinstance
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1202
1203
1204
1205
1206
1207
1208
1209
1210
```

```
@staticmethod
def is_model_request_node(
    node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
) -> TypeGuard[_agent_graph.ModelRequestNode[T, S]]:
    """Check if the node is a `ModelRequestNode`, narrowing the type if it is.

    This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
    """
    return isinstance(node, _agent_graph.ModelRequestNode)
```

```
@staticmethod
def is_model_request_node(
    node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
) -> TypeGuard[_agent_graph.ModelRequestNode[T, S]]:
    """Check if the node is a `ModelRequestNode`, narrowing the type if it is.

    This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
    """
    return isinstance(node, _agent_graph.ModelRequestNode)
```

#### is_call_tools_node

staticmethod

```
staticmethod
```

```
is_call_tools_node(
    node: AgentNode[T, S] | End[FinalResult[S]],
) -> TypeGuard[CallToolsNode[T, S]]
```

```
is_call_tools_node(
    node: AgentNode[T, S] | End[FinalResult[S]],
) -> TypeGuard[CallToolsNode[T, S]]
```

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[TypeGuard](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeGuard)

Check if the node is a CallToolsNode, narrowing the type if it is.

```
CallToolsNode
```

This method preserves the generic parameters while narrowing the type, unlike a direct call to isinstance.

```
isinstance
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1212
1213
1214
1215
1216
1217
1218
1219
1220
```

```
@staticmethod
def is_call_tools_node(
    node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
) -> TypeGuard[_agent_graph.CallToolsNode[T, S]]:
    """Check if the node is a `CallToolsNode`, narrowing the type if it is.

    This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
    """
    return isinstance(node, _agent_graph.CallToolsNode)
```

```
@staticmethod
def is_call_tools_node(
    node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
) -> TypeGuard[_agent_graph.CallToolsNode[T, S]]:
    """Check if the node is a `CallToolsNode`, narrowing the type if it is.

    This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
    """
    return isinstance(node, _agent_graph.CallToolsNode)
```

#### is_user_prompt_node

staticmethod

```
staticmethod
```

```
is_user_prompt_node(
    node: AgentNode[T, S] | End[FinalResult[S]],
) -> TypeGuard[UserPromptNode[T, S]]
```

```
is_user_prompt_node(
    node: AgentNode[T, S] | End[FinalResult[S]],
) -> TypeGuard[UserPromptNode[T, S]]
```

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[TypeGuard](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeGuard)

Check if the node is a UserPromptNode, narrowing the type if it is.

```
UserPromptNode
```

This method preserves the generic parameters while narrowing the type, unlike a direct call to isinstance.

```
isinstance
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1222
1223
1224
1225
1226
1227
1228
1229
1230
```

```
@staticmethod
def is_user_prompt_node(
    node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
) -> TypeGuard[_agent_graph.UserPromptNode[T, S]]:
    """Check if the node is a `UserPromptNode`, narrowing the type if it is.

    This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
    """
    return isinstance(node, _agent_graph.UserPromptNode)
```

```
@staticmethod
def is_user_prompt_node(
    node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
) -> TypeGuard[_agent_graph.UserPromptNode[T, S]]:
    """Check if the node is a `UserPromptNode`, narrowing the type if it is.

    This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
    """
    return isinstance(node, _agent_graph.UserPromptNode)
```

#### is_end_node

staticmethod

```
staticmethod
```

```
is_end_node(
    node: AgentNode[T, S] | End[FinalResult[S]],
) -> TypeGuard[End[FinalResult[S]]]
```

```
is_end_node(
    node: AgentNode[T, S] | End[FinalResult[S]],
) -> TypeGuard[End[FinalResult[S]]]
```

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[TypeGuard](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeGuard)

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

Check if the node is a End, narrowing the type if it is.

```
End
```

This method preserves the generic parameters while narrowing the type, unlike a direct call to isinstance.

```
isinstance
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1232
1233
1234
1235
1236
1237
1238
1239
1240
```

```
@staticmethod
def is_end_node(
    node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
) -> TypeGuard[End[result.FinalResult[S]]]:
    """Check if the node is a `End`, narrowing the type if it is.

    This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
    """
    return isinstance(node, End)
```

```
@staticmethod
def is_end_node(
    node: _agent_graph.AgentNode[T, S] | End[result.FinalResult[S]],
) -> TypeGuard[End[result.FinalResult[S]]]:
    """Check if the node is a `End`, narrowing the type if it is.

    This method preserves the generic parameters while narrowing the type, unlike a direct call to `isinstance`.
    """
    return isinstance(node, End)
```

### AgentRun

dataclass

```
dataclass
```

Bases: Generic[AgentDepsT, ResultDataT]

```
Generic[AgentDepsT, ResultDataT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

A stateful, async-iterable run of an Agent.

```
Agent
```

You generally obtain an AgentRun instance by calling async with my_agent.iter(...) as agent_run:.

```
AgentRun
```

```
async with my_agent.iter(...) as agent_run:
```

Once you have an instance, you can use it to iterate through the run's nodes as they execute. When an
End is reached, the run finishes and result
becomes available.

```
End
```

```
result
```

Example:
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    nodes = []
    # Iterate through the run, recording each node along the way:
    async with agent.iter('What is the capital of France?') as agent_run:
        async for node in agent_run:
            nodes.append(node)
    print(nodes)
    '''
    [
        ModelRequestNode(
            request=ModelRequest(
                parts=[
                    UserPromptPart(
                        content='What is the capital of France?',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    )
                ],
                kind='request',
            )
        ),
        CallToolsNode(
            model_response=ModelResponse(
                parts=[TextPart(content='Paris', part_kind='text')],
                model_name='gpt-4o',
                timestamp=datetime.datetime(...),
                kind='response',
            )
        ),
        End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
    ]
    '''
    print(agent_run.result.data)
    #> Paris

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    nodes = []
    # Iterate through the run, recording each node along the way:
    async with agent.iter('What is the capital of France?') as agent_run:
        async for node in agent_run:
            nodes.append(node)
    print(nodes)
    '''
    [
        ModelRequestNode(
            request=ModelRequest(
                parts=[
                    UserPromptPart(
                        content='What is the capital of France?',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    )
                ],
                kind='request',
            )
        ),
        CallToolsNode(
            model_response=ModelResponse(
                parts=[TextPart(content='Paris', part_kind='text')],
                model_name='gpt-4o',
                timestamp=datetime.datetime(...),
                kind='response',
            )
        ),
        End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
    ]
    '''
    print(agent_run.result.data)
    #> Paris
```

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    nodes = []
    # Iterate through the run, recording each node along the way:
    async with agent.iter('What is the capital of France?') as agent_run:
        async for node in agent_run:
            nodes.append(node)
    print(nodes)
    '''
    [
        ModelRequestNode(
            request=ModelRequest(
                parts=[
                    UserPromptPart(
                        content='What is the capital of France?',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    )
                ],
                kind='request',
            )
        ),
        CallToolsNode(
            model_response=ModelResponse(
                parts=[TextPart(content='Paris', part_kind='text')],
                model_name='gpt-4o',
                timestamp=datetime.datetime(...),
                kind='response',
            )
        ),
        End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
    ]
    '''
    print(agent_run.result.data)
    #> Paris
```

You can also manually drive the iteration using the next method for
more granular control.

```
next
```

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
1435
1436
1437
1438
1439
1440
1441
```

```
@dataclasses.dataclass(repr=False)
class AgentRun(Generic[AgentDepsT, ResultDataT]):
    """A stateful, async-iterable run of an [`Agent`][pydantic_ai.agent.Agent].

    You generally obtain an `AgentRun` instance by calling `async with my_agent.iter(...) as agent_run:`.

    Once you have an instance, you can use it to iterate through the run's nodes as they execute. When an
    [`End`][pydantic_graph.nodes.End] is reached, the run finishes and [`result`][pydantic_ai.agent.AgentRun.result]
    becomes available.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    async def main():
        nodes = []
        # Iterate through the run, recording each node along the way:
        async with agent.iter('What is the capital of France?') as agent_run:
            async for node in agent_run:
                nodes.append(node)
        print(nodes)
        '''
        [
            ModelRequestNode(
                request=ModelRequest(
                    parts=[
                        UserPromptPart(
                            content='What is the capital of France?',
                            timestamp=datetime.datetime(...),
                            part_kind='user-prompt',
                        )
                    ],
                    kind='request',
                )
            ),
            CallToolsNode(
                model_response=ModelResponse(
                    parts=[TextPart(content='Paris', part_kind='text')],
                    model_name='gpt-4o',
                    timestamp=datetime.datetime(...),
                    kind='response',
                )
            ),
            End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
        ]
        '''
        print(agent_run.result.data)
        #> Paris
    ```

    You can also manually drive the iteration using the [`next`][pydantic_ai.agent.AgentRun.next] method for
    more granular control.
    """

    _graph_run: GraphRun[
        _agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any], FinalResult[ResultDataT]
    ]

    @property
    def ctx(self) -> GraphRunContext[_agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any]]:
        """The current context of the agent run."""
        return GraphRunContext[_agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any]](
            self._graph_run.state, self._graph_run.deps
        )

    @property
    def next_node(
        self,
    ) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
        """The next node that will be run in the agent graph.

        This is the next node that will be used during async iteration, or if a node is not passed to `self.next(...)`.
        """
        next_node = self._graph_run.next_node
        if isinstance(next_node, End):
            return next_node
        if _agent_graph.is_agent_node(next_node):
            return next_node
        raise exceptions.AgentRunError(f'Unexpected node type: {type(next_node)}')  # pragma: no cover

    @property
    def result(self) -> AgentRunResult[ResultDataT] | None:
        """The final result of the run if it has ended, otherwise `None`.

        Once the run returns an [`End`][pydantic_graph.nodes.End] node, `result` is populated
        with an [`AgentRunResult`][pydantic_ai.agent.AgentRunResult].
        """
        graph_run_result = self._graph_run.result
        if graph_run_result is None:
            return None
        return AgentRunResult(
            graph_run_result.output.data,
            graph_run_result.output.tool_name,
            graph_run_result.state,
            self._graph_run.deps.new_message_index,
        )

    def __aiter__(
        self,
    ) -> AsyncIterator[_agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]]:
        """Provide async-iteration over the nodes in the agent run."""
        return self

    async def __anext__(
        self,
    ) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
        """Advance to the next node automatically based on the last returned node."""
        next_node = await self._graph_run.__anext__()
        if _agent_graph.is_agent_node(next_node):
            return next_node
        assert isinstance(next_node, End), f'Unexpected node type: {type(next_node)}'
        return next_node

    async def next(
        self,
        node: _agent_graph.AgentNode[AgentDepsT, ResultDataT],
    ) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
        """Manually drive the agent run by passing in the node you want to run next.

        This lets you inspect or mutate the node before continuing execution, or skip certain nodes
        under dynamic conditions. The agent run should be stopped when you return an [`End`][pydantic_graph.nodes.End]
        node.

        Example:
        ```python
        from pydantic_ai import Agent
        from pydantic_graph import End

        agent = Agent('openai:gpt-4o')

        async def main():
            async with agent.iter('What is the capital of France?') as agent_run:
                next_node = agent_run.next_node  # start with the first node
                nodes = [next_node]
                while not isinstance(next_node, End):
                    next_node = await agent_run.next(next_node)
                    nodes.append(next_node)
                # Once `next_node` is an End, we've finished:
                print(nodes)
                '''
                [
                    UserPromptNode(
                        user_prompt='What is the capital of France?',
                        system_prompts=(),
                        system_prompt_functions=[],
                        system_prompt_dynamic_functions={},
                    ),
                    ModelRequestNode(
                        request=ModelRequest(
                            parts=[
                                UserPromptPart(
                                    content='What is the capital of France?',
                                    timestamp=datetime.datetime(...),
                                    part_kind='user-prompt',
                                )
                            ],
                            kind='request',
                        )
                    ),
                    CallToolsNode(
                        model_response=ModelResponse(
                            parts=[TextPart(content='Paris', part_kind='text')],
                            model_name='gpt-4o',
                            timestamp=datetime.datetime(...),
                            kind='response',
                        )
                    ),
                    End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
                ]
                '''
                print('Final result:', agent_run.result.data)
                #> Final result: Paris
        ```

        Args:
            node: The node to run next in the graph.

        Returns:
            The next node returned by the graph logic, or an [`End`][pydantic_graph.nodes.End] node if
            the run has completed.
        """
        # Note: It might be nice to expose a synchronous interface for iteration, but we shouldn't do it
        # on this class, or else IDEs won't warn you if you accidentally use `for` instead of `async for` to iterate.
        next_node = await self._graph_run.next(node)
        if _agent_graph.is_agent_node(next_node):
            return next_node
        assert isinstance(next_node, End), f'Unexpected node type: {type(next_node)}'
        return next_node

    def usage(self) -> _usage.Usage:
        """Get usage statistics for the run so far, including token usage, model requests, and so on."""
        return self._graph_run.state.usage

    def __repr__(self) -> str:
        result = self._graph_run.result
        result_repr = '<run not finished>' if result is None else repr(result.output)
        return f'<{type(self).__name__} result={result_repr} usage={self.usage()}>'
```

```
@dataclasses.dataclass(repr=False)
class AgentRun(Generic[AgentDepsT, ResultDataT]):
    """A stateful, async-iterable run of an [`Agent`][pydantic_ai.agent.Agent].

    You generally obtain an `AgentRun` instance by calling `async with my_agent.iter(...) as agent_run:`.

    Once you have an instance, you can use it to iterate through the run's nodes as they execute. When an
    [`End`][pydantic_graph.nodes.End] is reached, the run finishes and [`result`][pydantic_ai.agent.AgentRun.result]
    becomes available.

    Example:
    ```python
    from pydantic_ai import Agent

    agent = Agent('openai:gpt-4o')

    async def main():
        nodes = []
        # Iterate through the run, recording each node along the way:
        async with agent.iter('What is the capital of France?') as agent_run:
            async for node in agent_run:
                nodes.append(node)
        print(nodes)
        '''
        [
            ModelRequestNode(
                request=ModelRequest(
                    parts=[
                        UserPromptPart(
                            content='What is the capital of France?',
                            timestamp=datetime.datetime(...),
                            part_kind='user-prompt',
                        )
                    ],
                    kind='request',
                )
            ),
            CallToolsNode(
                model_response=ModelResponse(
                    parts=[TextPart(content='Paris', part_kind='text')],
                    model_name='gpt-4o',
                    timestamp=datetime.datetime(...),
                    kind='response',
                )
            ),
            End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
        ]
        '''
        print(agent_run.result.data)
        #> Paris
    ```

    You can also manually drive the iteration using the [`next`][pydantic_ai.agent.AgentRun.next] method for
    more granular control.
    """

    _graph_run: GraphRun[
        _agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any], FinalResult[ResultDataT]
    ]

    @property
    def ctx(self) -> GraphRunContext[_agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any]]:
        """The current context of the agent run."""
        return GraphRunContext[_agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any]](
            self._graph_run.state, self._graph_run.deps
        )

    @property
    def next_node(
        self,
    ) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
        """The next node that will be run in the agent graph.

        This is the next node that will be used during async iteration, or if a node is not passed to `self.next(...)`.
        """
        next_node = self._graph_run.next_node
        if isinstance(next_node, End):
            return next_node
        if _agent_graph.is_agent_node(next_node):
            return next_node
        raise exceptions.AgentRunError(f'Unexpected node type: {type(next_node)}')  # pragma: no cover

    @property
    def result(self) -> AgentRunResult[ResultDataT] | None:
        """The final result of the run if it has ended, otherwise `None`.

        Once the run returns an [`End`][pydantic_graph.nodes.End] node, `result` is populated
        with an [`AgentRunResult`][pydantic_ai.agent.AgentRunResult].
        """
        graph_run_result = self._graph_run.result
        if graph_run_result is None:
            return None
        return AgentRunResult(
            graph_run_result.output.data,
            graph_run_result.output.tool_name,
            graph_run_result.state,
            self._graph_run.deps.new_message_index,
        )

    def __aiter__(
        self,
    ) -> AsyncIterator[_agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]]:
        """Provide async-iteration over the nodes in the agent run."""
        return self

    async def __anext__(
        self,
    ) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
        """Advance to the next node automatically based on the last returned node."""
        next_node = await self._graph_run.__anext__()
        if _agent_graph.is_agent_node(next_node):
            return next_node
        assert isinstance(next_node, End), f'Unexpected node type: {type(next_node)}'
        return next_node

    async def next(
        self,
        node: _agent_graph.AgentNode[AgentDepsT, ResultDataT],
    ) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
        """Manually drive the agent run by passing in the node you want to run next.

        This lets you inspect or mutate the node before continuing execution, or skip certain nodes
        under dynamic conditions. The agent run should be stopped when you return an [`End`][pydantic_graph.nodes.End]
        node.

        Example:
        ```python
        from pydantic_ai import Agent
        from pydantic_graph import End

        agent = Agent('openai:gpt-4o')

        async def main():
            async with agent.iter('What is the capital of France?') as agent_run:
                next_node = agent_run.next_node  # start with the first node
                nodes = [next_node]
                while not isinstance(next_node, End):
                    next_node = await agent_run.next(next_node)
                    nodes.append(next_node)
                # Once `next_node` is an End, we've finished:
                print(nodes)
                '''
                [
                    UserPromptNode(
                        user_prompt='What is the capital of France?',
                        system_prompts=(),
                        system_prompt_functions=[],
                        system_prompt_dynamic_functions={},
                    ),
                    ModelRequestNode(
                        request=ModelRequest(
                            parts=[
                                UserPromptPart(
                                    content='What is the capital of France?',
                                    timestamp=datetime.datetime(...),
                                    part_kind='user-prompt',
                                )
                            ],
                            kind='request',
                        )
                    ),
                    CallToolsNode(
                        model_response=ModelResponse(
                            parts=[TextPart(content='Paris', part_kind='text')],
                            model_name='gpt-4o',
                            timestamp=datetime.datetime(...),
                            kind='response',
                        )
                    ),
                    End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
                ]
                '''
                print('Final result:', agent_run.result.data)
                #> Final result: Paris
        ```

        Args:
            node: The node to run next in the graph.

        Returns:
            The next node returned by the graph logic, or an [`End`][pydantic_graph.nodes.End] node if
            the run has completed.
        """
        # Note: It might be nice to expose a synchronous interface for iteration, but we shouldn't do it
        # on this class, or else IDEs won't warn you if you accidentally use `for` instead of `async for` to iterate.
        next_node = await self._graph_run.next(node)
        if _agent_graph.is_agent_node(next_node):
            return next_node
        assert isinstance(next_node, End), f'Unexpected node type: {type(next_node)}'
        return next_node

    def usage(self) -> _usage.Usage:
        """Get usage statistics for the run so far, including token usage, model requests, and so on."""
        return self._graph_run.state.usage

    def __repr__(self) -> str:
        result = self._graph_run.result
        result_repr = '<run not finished>' if result is None else repr(result.output)
        return f'<{type(self).__name__} result={result_repr} usage={self.usage()}>'
```

#### ctx

property

```
property
```

```
ctx: GraphRunContext[
    GraphAgentState, GraphAgentDeps[AgentDepsT, Any]
]
```

```
ctx: GraphRunContext[
    GraphAgentState, GraphAgentDeps[AgentDepsT, Any]
]
```

[GraphRunContext](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.GraphRunContext)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

The current context of the agent run.

#### next_node

property

```
property
```

```
next_node: (
    AgentNode[AgentDepsT, ResultDataT]
    | End[FinalResult[ResultDataT]]
)
```

```
next_node: (
    AgentNode[AgentDepsT, ResultDataT]
    | End[FinalResult[ResultDataT]]
)
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

The next node that will be run in the agent graph.

This is the next node that will be used during async iteration, or if a node is not passed to self.next(...).

```
self.next(...)
```

#### result

property

```
property
```

```
result: AgentRunResult[ResultDataT] | None
```

```
result: AgentRunResult[ResultDataT] | None
```

[AgentRunResult](https://ai.pydantic.dev#pydantic_ai.agent.AgentRunResult)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

The final result of the run if it has ended, otherwise None.

```
None
```

Once the run returns an End node, result is populated
with an AgentRunResult.

```
End
```

```
result
```

```
AgentRunResult
```

#### __aiter__

```
__aiter__() -> (
    AsyncIterator[
        AgentNode[AgentDepsT, ResultDataT]
        | End[FinalResult[ResultDataT]]
    ]
)
```

```
__aiter__() -> (
    AsyncIterator[
        AgentNode[AgentDepsT, ResultDataT]
        | End[FinalResult[ResultDataT]]
    ]
)
```

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

Provide async-iteration over the nodes in the agent run.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1342
1343
1344
1345
1346
```

```
def __aiter__(
    self,
) -> AsyncIterator[_agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]]:
    """Provide async-iteration over the nodes in the agent run."""
    return self
```

```
def __aiter__(
    self,
) -> AsyncIterator[_agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]]:
    """Provide async-iteration over the nodes in the agent run."""
    return self
```

#### __anext__

async

```
async
```

```
__anext__() -> (
    AgentNode[AgentDepsT, ResultDataT]
    | End[FinalResult[ResultDataT]]
)
```

```
__anext__() -> (
    AgentNode[AgentDepsT, ResultDataT]
    | End[FinalResult[ResultDataT]]
)
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

Advance to the next node automatically based on the last returned node.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1348
1349
1350
1351
1352
1353
1354
1355
1356
```

```
async def __anext__(
    self,
) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
    """Advance to the next node automatically based on the last returned node."""
    next_node = await self._graph_run.__anext__()
    if _agent_graph.is_agent_node(next_node):
        return next_node
    assert isinstance(next_node, End), f'Unexpected node type: {type(next_node)}'
    return next_node
```

```
async def __anext__(
    self,
) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
    """Advance to the next node automatically based on the last returned node."""
    next_node = await self._graph_run.__anext__()
    if _agent_graph.is_agent_node(next_node):
        return next_node
    assert isinstance(next_node, End), f'Unexpected node type: {type(next_node)}'
    return next_node
```

#### next

async

```
async
```

```
next(
    node: AgentNode[AgentDepsT, ResultDataT],
) -> (
    AgentNode[AgentDepsT, ResultDataT]
    | End[FinalResult[ResultDataT]]
)
```

```
next(
    node: AgentNode[AgentDepsT, ResultDataT],
) -> (
    AgentNode[AgentDepsT, ResultDataT]
    | End[FinalResult[ResultDataT]]
)
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

Manually drive the agent run by passing in the node you want to run next.

This lets you inspect or mutate the node before continuing execution, or skip certain nodes
under dynamic conditions. The agent run should be stopped when you return an End
node.

```
End
```

Example:
from pydantic_ai import Agent
from pydantic_graph import End

agent = Agent('openai:gpt-4o')

async def main():
    async with agent.iter('What is the capital of France?') as agent_run:
        next_node = agent_run.next_node  # start with the first node
        nodes = [next_node]
        while not isinstance(next_node, End):
            next_node = await agent_run.next(next_node)
            nodes.append(next_node)
        # Once `next_node` is an End, we've finished:
        print(nodes)
        '''
        [
            UserPromptNode(
                user_prompt='What is the capital of France?',
                system_prompts=(),
                system_prompt_functions=[],
                system_prompt_dynamic_functions={},
            ),
            ModelRequestNode(
                request=ModelRequest(
                    parts=[
                        UserPromptPart(
                            content='What is the capital of France?',
                            timestamp=datetime.datetime(...),
                            part_kind='user-prompt',
                        )
                    ],
                    kind='request',
                )
            ),
            CallToolsNode(
                model_response=ModelResponse(
                    parts=[TextPart(content='Paris', part_kind='text')],
                    model_name='gpt-4o',
                    timestamp=datetime.datetime(...),
                    kind='response',
                )
            ),
            End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
        ]
        '''
        print('Final result:', agent_run.result.data)
        #> Final result: Paris

```
from pydantic_ai import Agent
from pydantic_graph import End

agent = Agent('openai:gpt-4o')

async def main():
    async with agent.iter('What is the capital of France?') as agent_run:
        next_node = agent_run.next_node  # start with the first node
        nodes = [next_node]
        while not isinstance(next_node, End):
            next_node = await agent_run.next(next_node)
            nodes.append(next_node)
        # Once `next_node` is an End, we've finished:
        print(nodes)
        '''
        [
            UserPromptNode(
                user_prompt='What is the capital of France?',
                system_prompts=(),
                system_prompt_functions=[],
                system_prompt_dynamic_functions={},
            ),
            ModelRequestNode(
                request=ModelRequest(
                    parts=[
                        UserPromptPart(
                            content='What is the capital of France?',
                            timestamp=datetime.datetime(...),
                            part_kind='user-prompt',
                        )
                    ],
                    kind='request',
                )
            ),
            CallToolsNode(
                model_response=ModelResponse(
                    parts=[TextPart(content='Paris', part_kind='text')],
                    model_name='gpt-4o',
                    timestamp=datetime.datetime(...),
                    kind='response',
                )
            ),
            End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
        ]
        '''
        print('Final result:', agent_run.result.data)
        #> Final result: Paris
```

```
from pydantic_ai import Agent
from pydantic_graph import End

agent = Agent('openai:gpt-4o')

async def main():
    async with agent.iter('What is the capital of France?') as agent_run:
        next_node = agent_run.next_node  # start with the first node
        nodes = [next_node]
        while not isinstance(next_node, End):
            next_node = await agent_run.next(next_node)
            nodes.append(next_node)
        # Once `next_node` is an End, we've finished:
        print(nodes)
        '''
        [
            UserPromptNode(
                user_prompt='What is the capital of France?',
                system_prompts=(),
                system_prompt_functions=[],
                system_prompt_dynamic_functions={},
            ),
            ModelRequestNode(
                request=ModelRequest(
                    parts=[
                        UserPromptPart(
                            content='What is the capital of France?',
                            timestamp=datetime.datetime(...),
                            part_kind='user-prompt',
                        )
                    ],
                    kind='request',
                )
            ),
            CallToolsNode(
                model_response=ModelResponse(
                    parts=[TextPart(content='Paris', part_kind='text')],
                    model_name='gpt-4o',
                    timestamp=datetime.datetime(...),
                    kind='response',
                )
            ),
            End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
        ]
        '''
        print('Final result:', agent_run.result.data)
        #> Final result: Paris
```

Parameters:

```
node
```

```
AgentNode[AgentDepsT, ResultDataT]
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

The node to run next in the graph.

Returns:

```
AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

The next node returned by the graph logic, or an End node if

```
End
```

```
AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]
```

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

[End](https://ai.pydantic.dev/pydantic_graph/nodes/#pydantic_graph.nodes.End)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

the run has completed.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
```

```
async def next(
    self,
    node: _agent_graph.AgentNode[AgentDepsT, ResultDataT],
) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
    """Manually drive the agent run by passing in the node you want to run next.

    This lets you inspect or mutate the node before continuing execution, or skip certain nodes
    under dynamic conditions. The agent run should be stopped when you return an [`End`][pydantic_graph.nodes.End]
    node.

    Example:
    ```python
    from pydantic_ai import Agent
    from pydantic_graph import End

    agent = Agent('openai:gpt-4o')

    async def main():
        async with agent.iter('What is the capital of France?') as agent_run:
            next_node = agent_run.next_node  # start with the first node
            nodes = [next_node]
            while not isinstance(next_node, End):
                next_node = await agent_run.next(next_node)
                nodes.append(next_node)
            # Once `next_node` is an End, we've finished:
            print(nodes)
            '''
            [
                UserPromptNode(
                    user_prompt='What is the capital of France?',
                    system_prompts=(),
                    system_prompt_functions=[],
                    system_prompt_dynamic_functions={},
                ),
                ModelRequestNode(
                    request=ModelRequest(
                        parts=[
                            UserPromptPart(
                                content='What is the capital of France?',
                                timestamp=datetime.datetime(...),
                                part_kind='user-prompt',
                            )
                        ],
                        kind='request',
                    )
                ),
                CallToolsNode(
                    model_response=ModelResponse(
                        parts=[TextPart(content='Paris', part_kind='text')],
                        model_name='gpt-4o',
                        timestamp=datetime.datetime(...),
                        kind='response',
                    )
                ),
                End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
            ]
            '''
            print('Final result:', agent_run.result.data)
            #> Final result: Paris
    ```

    Args:
        node: The node to run next in the graph.

    Returns:
        The next node returned by the graph logic, or an [`End`][pydantic_graph.nodes.End] node if
        the run has completed.
    """
    # Note: It might be nice to expose a synchronous interface for iteration, but we shouldn't do it
    # on this class, or else IDEs won't warn you if you accidentally use `for` instead of `async for` to iterate.
    next_node = await self._graph_run.next(node)
    if _agent_graph.is_agent_node(next_node):
        return next_node
    assert isinstance(next_node, End), f'Unexpected node type: {type(next_node)}'
    return next_node
```

```
async def next(
    self,
    node: _agent_graph.AgentNode[AgentDepsT, ResultDataT],
) -> _agent_graph.AgentNode[AgentDepsT, ResultDataT] | End[FinalResult[ResultDataT]]:
    """Manually drive the agent run by passing in the node you want to run next.

    This lets you inspect or mutate the node before continuing execution, or skip certain nodes
    under dynamic conditions. The agent run should be stopped when you return an [`End`][pydantic_graph.nodes.End]
    node.

    Example:
    ```python
    from pydantic_ai import Agent
    from pydantic_graph import End

    agent = Agent('openai:gpt-4o')

    async def main():
        async with agent.iter('What is the capital of France?') as agent_run:
            next_node = agent_run.next_node  # start with the first node
            nodes = [next_node]
            while not isinstance(next_node, End):
                next_node = await agent_run.next(next_node)
                nodes.append(next_node)
            # Once `next_node` is an End, we've finished:
            print(nodes)
            '''
            [
                UserPromptNode(
                    user_prompt='What is the capital of France?',
                    system_prompts=(),
                    system_prompt_functions=[],
                    system_prompt_dynamic_functions={},
                ),
                ModelRequestNode(
                    request=ModelRequest(
                        parts=[
                            UserPromptPart(
                                content='What is the capital of France?',
                                timestamp=datetime.datetime(...),
                                part_kind='user-prompt',
                            )
                        ],
                        kind='request',
                    )
                ),
                CallToolsNode(
                    model_response=ModelResponse(
                        parts=[TextPart(content='Paris', part_kind='text')],
                        model_name='gpt-4o',
                        timestamp=datetime.datetime(...),
                        kind='response',
                    )
                ),
                End(data=FinalResult(data='Paris', tool_name=None, tool_call_id=None)),
            ]
            '''
            print('Final result:', agent_run.result.data)
            #> Final result: Paris
    ```

    Args:
        node: The node to run next in the graph.

    Returns:
        The next node returned by the graph logic, or an [`End`][pydantic_graph.nodes.End] node if
        the run has completed.
    """
    # Note: It might be nice to expose a synchronous interface for iteration, but we shouldn't do it
    # on this class, or else IDEs won't warn you if you accidentally use `for` instead of `async for` to iterate.
    next_node = await self._graph_run.next(node)
    if _agent_graph.is_agent_node(next_node):
        return next_node
    assert isinstance(next_node, End), f'Unexpected node type: {type(next_node)}'
    return next_node
```

#### usage

```
usage() -> Usage
```

```
usage() -> Usage
```

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

Get usage statistics for the run so far, including token usage, model requests, and so on.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1434
1435
1436
```

```
def usage(self) -> _usage.Usage:
    """Get usage statistics for the run so far, including token usage, model requests, and so on."""
    return self._graph_run.state.usage
```

```
def usage(self) -> _usage.Usage:
    """Get usage statistics for the run so far, including token usage, model requests, and so on."""
    return self._graph_run.state.usage
```

### AgentRunResult

dataclass

```
dataclass
```

Bases: Generic[ResultDataT]

```
Generic[ResultDataT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[ResultDataT](https://ai.pydantic.dev/result/#pydantic_ai.result.ResultDataT)

The final result of an agent run.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1444
1445
1446
1447
1448
1449
1450
1451
1452
1453
1454
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
1529
1530
1531
1532
1533
1534
1535
1536
```

```
@dataclasses.dataclass
class AgentRunResult(Generic[ResultDataT]):
    """The final result of an agent run."""

    data: ResultDataT  # TODO: rename this to output. I'm putting this off for now mostly to reduce the size of the diff

    _result_tool_name: str | None = dataclasses.field(repr=False)
    _state: _agent_graph.GraphAgentState = dataclasses.field(repr=False)
    _new_message_index: int = dataclasses.field(repr=False)

    def _set_result_tool_return(self, return_content: str) -> list[_messages.ModelMessage]:
        """Set return content for the result tool.

        Useful if you want to continue the conversation and want to set the response to the result tool call.
        """
        if not self._result_tool_name:
            raise ValueError('Cannot set result tool return content when the return type is `str`.')
        messages = deepcopy(self._state.message_history)
        last_message = messages[-1]
        for part in last_message.parts:
            if isinstance(part, _messages.ToolReturnPart) and part.tool_name == self._result_tool_name:
                part.content = return_content
                return messages
        raise LookupError(f'No tool call found with tool name {self._result_tool_name!r}.')

    def all_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
        """Return the history of _messages.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            List of messages.
        """
        if result_tool_return_content is not None:
            return self._set_result_tool_return(result_tool_return_content)
        else:
            return self._state.message_history

    def all_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
        """Return all messages from [`all_messages`][pydantic_ai.agent.AgentRunResult.all_messages] as JSON bytes.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            JSON bytes representing the messages.
        """
        return _messages.ModelMessagesTypeAdapter.dump_json(
            self.all_messages(result_tool_return_content=result_tool_return_content)
        )

    def new_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
        """Return new messages associated with this run.

        Messages from older runs are excluded.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            List of new messages.
        """
        return self.all_messages(result_tool_return_content=result_tool_return_content)[self._new_message_index :]

    def new_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
        """Return new messages from [`new_messages`][pydantic_ai.agent.AgentRunResult.new_messages] as JSON bytes.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            JSON bytes representing the new messages.
        """
        return _messages.ModelMessagesTypeAdapter.dump_json(
            self.new_messages(result_tool_return_content=result_tool_return_content)
        )

    def usage(self) -> _usage.Usage:
        """Return the usage of the whole run."""
        return self._state.usage
```

```
@dataclasses.dataclass
class AgentRunResult(Generic[ResultDataT]):
    """The final result of an agent run."""

    data: ResultDataT  # TODO: rename this to output. I'm putting this off for now mostly to reduce the size of the diff

    _result_tool_name: str | None = dataclasses.field(repr=False)
    _state: _agent_graph.GraphAgentState = dataclasses.field(repr=False)
    _new_message_index: int = dataclasses.field(repr=False)

    def _set_result_tool_return(self, return_content: str) -> list[_messages.ModelMessage]:
        """Set return content for the result tool.

        Useful if you want to continue the conversation and want to set the response to the result tool call.
        """
        if not self._result_tool_name:
            raise ValueError('Cannot set result tool return content when the return type is `str`.')
        messages = deepcopy(self._state.message_history)
        last_message = messages[-1]
        for part in last_message.parts:
            if isinstance(part, _messages.ToolReturnPart) and part.tool_name == self._result_tool_name:
                part.content = return_content
                return messages
        raise LookupError(f'No tool call found with tool name {self._result_tool_name!r}.')

    def all_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
        """Return the history of _messages.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            List of messages.
        """
        if result_tool_return_content is not None:
            return self._set_result_tool_return(result_tool_return_content)
        else:
            return self._state.message_history

    def all_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
        """Return all messages from [`all_messages`][pydantic_ai.agent.AgentRunResult.all_messages] as JSON bytes.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            JSON bytes representing the messages.
        """
        return _messages.ModelMessagesTypeAdapter.dump_json(
            self.all_messages(result_tool_return_content=result_tool_return_content)
        )

    def new_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
        """Return new messages associated with this run.

        Messages from older runs are excluded.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            List of new messages.
        """
        return self.all_messages(result_tool_return_content=result_tool_return_content)[self._new_message_index :]

    def new_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
        """Return new messages from [`new_messages`][pydantic_ai.agent.AgentRunResult.new_messages] as JSON bytes.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            JSON bytes representing the new messages.
        """
        return _messages.ModelMessagesTypeAdapter.dump_json(
            self.new_messages(result_tool_return_content=result_tool_return_content)
        )

    def usage(self) -> _usage.Usage:
        """Return the usage of the whole run."""
        return self._state.usage
```

#### all_messages

```
all_messages(
    *, result_tool_return_content: str | None = None
) -> list[ModelMessage]
```

```
all_messages(
    *, result_tool_return_content: str | None = None
) -> list[ModelMessage]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

Return the history of _messages.

Parameters:

```
result_tool_return_content
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The return content of the tool call to set in the last message.
This provides a convenient way to modify the content of the result tool call if you want to continue
the conversation and want to set the response to the result tool call. If None, the last message will
not be modified.

```
None
```

```
None
```

Returns:

```
list[ModelMessage]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

List of messages.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
```

```
def all_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
    """Return the history of _messages.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        List of messages.
    """
    if result_tool_return_content is not None:
        return self._set_result_tool_return(result_tool_return_content)
    else:
        return self._state.message_history
```

```
def all_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
    """Return the history of _messages.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        List of messages.
    """
    if result_tool_return_content is not None:
        return self._set_result_tool_return(result_tool_return_content)
    else:
        return self._state.message_history
```

#### all_messages_json

```
all_messages_json(
    *, result_tool_return_content: str | None = None
) -> bytes
```

```
all_messages_json(
    *, result_tool_return_content: str | None = None
) -> bytes
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

Return all messages from all_messages as JSON bytes.

```
all_messages
```

Parameters:

```
result_tool_return_content
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The return content of the tool call to set in the last message.
This provides a convenient way to modify the content of the result tool call if you want to continue
the conversation and want to set the response to the result tool call. If None, the last message will
not be modified.

```
None
```

```
None
```

Returns:

```
bytes
```

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

JSON bytes representing the messages.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
```

```
def all_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
    """Return all messages from [`all_messages`][pydantic_ai.agent.AgentRunResult.all_messages] as JSON bytes.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        JSON bytes representing the messages.
    """
    return _messages.ModelMessagesTypeAdapter.dump_json(
        self.all_messages(result_tool_return_content=result_tool_return_content)
    )
```

```
def all_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
    """Return all messages from [`all_messages`][pydantic_ai.agent.AgentRunResult.all_messages] as JSON bytes.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        JSON bytes representing the messages.
    """
    return _messages.ModelMessagesTypeAdapter.dump_json(
        self.all_messages(result_tool_return_content=result_tool_return_content)
    )
```

#### new_messages

```
new_messages(
    *, result_tool_return_content: str | None = None
) -> list[ModelMessage]
```

```
new_messages(
    *, result_tool_return_content: str | None = None
) -> list[ModelMessage]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

Return new messages associated with this run.

Messages from older runs are excluded.

Parameters:

```
result_tool_return_content
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The return content of the tool call to set in the last message.
This provides a convenient way to modify the content of the result tool call if you want to continue
the conversation and want to set the response to the result tool call. If None, the last message will
not be modified.

```
None
```

```
None
```

Returns:

```
list[ModelMessage]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

List of new messages.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
```

```
def new_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
    """Return new messages associated with this run.

    Messages from older runs are excluded.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        List of new messages.
    """
    return self.all_messages(result_tool_return_content=result_tool_return_content)[self._new_message_index :]
```

```
def new_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
    """Return new messages associated with this run.

    Messages from older runs are excluded.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        List of new messages.
    """
    return self.all_messages(result_tool_return_content=result_tool_return_content)[self._new_message_index :]
```

#### new_messages_json

```
new_messages_json(
    *, result_tool_return_content: str | None = None
) -> bytes
```

```
new_messages_json(
    *, result_tool_return_content: str | None = None
) -> bytes
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

Return new messages from new_messages as JSON bytes.

```
new_messages
```

Parameters:

```
result_tool_return_content
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The return content of the tool call to set in the last message.
This provides a convenient way to modify the content of the result tool call if you want to continue
the conversation and want to set the response to the result tool call. If None, the last message will
not be modified.

```
None
```

```
None
```

Returns:

```
bytes
```

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

JSON bytes representing the new messages.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
1529
1530
1531
1532
```

```
def new_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
    """Return new messages from [`new_messages`][pydantic_ai.agent.AgentRunResult.new_messages] as JSON bytes.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        JSON bytes representing the new messages.
    """
    return _messages.ModelMessagesTypeAdapter.dump_json(
        self.new_messages(result_tool_return_content=result_tool_return_content)
    )
```

```
def new_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
    """Return new messages from [`new_messages`][pydantic_ai.agent.AgentRunResult.new_messages] as JSON bytes.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        JSON bytes representing the new messages.
    """
    return _messages.ModelMessagesTypeAdapter.dump_json(
        self.new_messages(result_tool_return_content=result_tool_return_content)
    )
```

#### usage

```
usage() -> Usage
```

```
usage() -> Usage
```

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

Return the usage of the whole run.

```
pydantic_ai_slim/pydantic_ai/agent.py
```

```
1534
1535
1536
```

```
def usage(self) -> _usage.Usage:
    """Return the usage of the whole run."""
    return self._state.usage
```

```
def usage(self) -> _usage.Usage:
    """Return the usage of the whole run."""
    return self._state.usage
```

### EndStrategy

module-attribute

```
module-attribute
```

```
EndStrategy = EndStrategy
```

```
EndStrategy = EndStrategy
```

### RunResultDataT

module-attribute

```
module-attribute
```

```
RunResultDataT = TypeVar('RunResultDataT')
```

```
RunResultDataT = TypeVar('RunResultDataT')
```

Type variable for the result data of a run where result_type was customized on the run call.

```
result_type
```

### capture_run_messages

module-attribute

```
module-attribute
```

```
capture_run_messages = capture_run_messages
```

```
capture_run_messages = capture_run_messages
```

### InstrumentationSettings

dataclass

```
dataclass
```

Options for instrumenting models and agents with OpenTelemetry.

Used in:

* Agent(instrument=...)
* Agent.instrument_all()
* InstrumentedModel

```
Agent(instrument=...)
```

```
Agent.instrument_all()
```

```
InstrumentedModel
```

```
pydantic_ai_slim/pydantic_ai/models/instrumented.py
```

```
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
```

```
@dataclass(init=False)
class InstrumentationSettings:
    """Options for instrumenting models and agents with OpenTelemetry.

    Used in:

    - `Agent(instrument=...)`
    - [`Agent.instrument_all()`][pydantic_ai.agent.Agent.instrument_all]
    - `InstrumentedModel`
    """

    tracer: Tracer = field(repr=False)
    event_logger: EventLogger = field(repr=False)
    event_mode: Literal['attributes', 'logs'] = 'attributes'

    def __init__(
        self,
        *,
        event_mode: Literal['attributes', 'logs'] = 'attributes',
        tracer_provider: TracerProvider | None = None,
        event_logger_provider: EventLoggerProvider | None = None,
    ):
        """Create instrumentation options.

        Args:
            event_mode: The mode for emitting events. If `'attributes'`, events are attached to the span as attributes.
                If `'logs'`, events are emitted as OpenTelemetry log-based events.
            tracer_provider: The OpenTelemetry tracer provider to use.
                If not provided, the global tracer provider is used.
                Calling `logfire.configure()` sets the global tracer provider, so most users don't need this.
            event_logger_provider: The OpenTelemetry event logger provider to use.
                If not provided, the global event logger provider is used.
                Calling `logfire.configure()` sets the global event logger provider, so most users don't need this.
                This is only used if `event_mode='logs'`.
        """
        from pydantic_ai import __version__

        tracer_provider = tracer_provider or get_tracer_provider()
        event_logger_provider = event_logger_provider or get_event_logger_provider()
        self.tracer = tracer_provider.get_tracer('pydantic-ai', __version__)
        self.event_logger = event_logger_provider.get_event_logger('pydantic-ai', __version__)
        self.event_mode = event_mode
```

```
@dataclass(init=False)
class InstrumentationSettings:
    """Options for instrumenting models and agents with OpenTelemetry.

    Used in:

    - `Agent(instrument=...)`
    - [`Agent.instrument_all()`][pydantic_ai.agent.Agent.instrument_all]
    - `InstrumentedModel`
    """

    tracer: Tracer = field(repr=False)
    event_logger: EventLogger = field(repr=False)
    event_mode: Literal['attributes', 'logs'] = 'attributes'

    def __init__(
        self,
        *,
        event_mode: Literal['attributes', 'logs'] = 'attributes',
        tracer_provider: TracerProvider | None = None,
        event_logger_provider: EventLoggerProvider | None = None,
    ):
        """Create instrumentation options.

        Args:
            event_mode: The mode for emitting events. If `'attributes'`, events are attached to the span as attributes.
                If `'logs'`, events are emitted as OpenTelemetry log-based events.
            tracer_provider: The OpenTelemetry tracer provider to use.
                If not provided, the global tracer provider is used.
                Calling `logfire.configure()` sets the global tracer provider, so most users don't need this.
            event_logger_provider: The OpenTelemetry event logger provider to use.
                If not provided, the global event logger provider is used.
                Calling `logfire.configure()` sets the global event logger provider, so most users don't need this.
                This is only used if `event_mode='logs'`.
        """
        from pydantic_ai import __version__

        tracer_provider = tracer_provider or get_tracer_provider()
        event_logger_provider = event_logger_provider or get_event_logger_provider()
        self.tracer = tracer_provider.get_tracer('pydantic-ai', __version__)
        self.event_logger = event_logger_provider.get_event_logger('pydantic-ai', __version__)
        self.event_mode = event_mode
```

#### __init__

```
__init__(
    *,
    event_mode: Literal[
        "attributes", "logs"
    ] = "attributes",
    tracer_provider: TracerProvider | None = None,
    event_logger_provider: EventLoggerProvider | None = None
)
```

```
__init__(
    *,
    event_mode: Literal[
        "attributes", "logs"
    ] = "attributes",
    tracer_provider: TracerProvider | None = None,
    event_logger_provider: EventLoggerProvider | None = None
)
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

Create instrumentation options.

Parameters:

```
event_mode
```

```
Literal['attributes', 'logs']
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

The mode for emitting events. If 'attributes', events are attached to the span as attributes.
If 'logs', events are emitted as OpenTelemetry log-based events.

```
'attributes'
```

```
'logs'
```

```
'attributes'
```

```
tracer_provider
```

```
TracerProvider | None
```

The OpenTelemetry tracer provider to use.
If not provided, the global tracer provider is used.
Calling logfire.configure() sets the global tracer provider, so most users don't need this.

```
logfire.configure()
```

```
None
```

```
event_logger_provider
```

```
EventLoggerProvider | None
```

The OpenTelemetry event logger provider to use.
If not provided, the global event logger provider is used.
Calling logfire.configure() sets the global event logger provider, so most users don't need this.
This is only used if event_mode='logs'.

```
logfire.configure()
```

```
event_mode='logs'
```

```
None
```

```
pydantic_ai_slim/pydantic_ai/models/instrumented.py
```

```
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
```

```
def __init__(
    self,
    *,
    event_mode: Literal['attributes', 'logs'] = 'attributes',
    tracer_provider: TracerProvider | None = None,
    event_logger_provider: EventLoggerProvider | None = None,
):
    """Create instrumentation options.

    Args:
        event_mode: The mode for emitting events. If `'attributes'`, events are attached to the span as attributes.
            If `'logs'`, events are emitted as OpenTelemetry log-based events.
        tracer_provider: The OpenTelemetry tracer provider to use.
            If not provided, the global tracer provider is used.
            Calling `logfire.configure()` sets the global tracer provider, so most users don't need this.
        event_logger_provider: The OpenTelemetry event logger provider to use.
            If not provided, the global event logger provider is used.
            Calling `logfire.configure()` sets the global event logger provider, so most users don't need this.
            This is only used if `event_mode='logs'`.
    """
    from pydantic_ai import __version__

    tracer_provider = tracer_provider or get_tracer_provider()
    event_logger_provider = event_logger_provider or get_event_logger_provider()
    self.tracer = tracer_provider.get_tracer('pydantic-ai', __version__)
    self.event_logger = event_logger_provider.get_event_logger('pydantic-ai', __version__)
    self.event_mode = event_mode
```

```
def __init__(
    self,
    *,
    event_mode: Literal['attributes', 'logs'] = 'attributes',
    tracer_provider: TracerProvider | None = None,
    event_logger_provider: EventLoggerProvider | None = None,
):
    """Create instrumentation options.

    Args:
        event_mode: The mode for emitting events. If `'attributes'`, events are attached to the span as attributes.
            If `'logs'`, events are emitted as OpenTelemetry log-based events.
        tracer_provider: The OpenTelemetry tracer provider to use.
            If not provided, the global tracer provider is used.
            Calling `logfire.configure()` sets the global tracer provider, so most users don't need this.
        event_logger_provider: The OpenTelemetry event logger provider to use.
            If not provided, the global event logger provider is used.
            Calling `logfire.configure()` sets the global event logger provider, so most users don't need this.
            This is only used if `event_mode='logs'`.
    """
    from pydantic_ai import __version__

    tracer_provider = tracer_provider or get_tracer_provider()
    event_logger_provider = event_logger_provider or get_event_logger_provider()
    self.tracer = tracer_provider.get_tracer('pydantic-ai', __version__)
    self.event_logger = event_logger_provider.get_event_logger('pydantic-ai', __version__)
    self.event_mode = event_mode
```

